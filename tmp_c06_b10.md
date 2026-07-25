以下是完整工作流。它是 Beacon Health AI 的 CodeReview Bot（非 PHI 功能；临床笔记摘要器有额外的 PHI 沙箱步骤，我们不会倾倒到这个通用模板中）的生产门禁。

    # .github/workflows/eval.yml
    name: Eval Suite

    on:
      pull_request:
        paths:
          - 'prompts/**'
          - 'src/**'
          - 'goldens/**'
          - '.github/workflows/eval.yml'
      push:
        branches: [main]

    jobs:
      eval:
        runs-on: ubuntu-latest
        timeout-minutes: 30
        permissions:
          contents: read
          pull-requests: write
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY_EVAL }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY_EVAL }}
        steps:
          - name: Checkout
            uses: actions/checkout@v4
            with:
              fetch-depth: 2

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.12'
              cache: 'pip'

          - name: Install dependencies
            run: |
              pip install -r requirements.txt
              pip install pytest-evals

          - name: Determine baseline SHA
            id: baseline
            run: |
              if [ "${{ github.event_name }}" = "pull_request" ]; then
                echo "sha=${{ github.event.pull_request.base.sha }}" >> $GITHUB_OUTPUT
              else
                echo "sha=${{ github.event.before }}" >> $GITHUB_OUTPUT
              fi

          - name: Run eval suite (candidate)
            id: candidate
            run: |
              python -m pytest tests/evals/ \
                --eval-output=eval_results_candidate.json \
                --eval-store=eval_store.sqlite \
                --git-sha=${{ github.sha }} \
                --prompt-version=$(cat prompts/version.txt) \
                --model-version=claude-sonnet-4-20260315

          - name: Run eval suite (baseline)
            id: baseline_run
            run: |
              git checkout ${{ steps.baseline.outputs.sha }} -- prompts/ src/
              python -m pytest tests/evals/ \
                --eval-output=eval_results_baseline.json \
                --eval-store=eval_store.sqlite \
                --git-sha=${{ steps.baseline.outputs.sha }} \
                --prompt-version=$(cat prompts/version.txt) \
                --model-version=claude-sonnet-4-20260315
              git checkout ${{ github.sha }} -- prompts/ src/

          - name: Compare and gate
            id: compare
            run: |
              python scripts/compare_evals.py \
                --candidate eval_results_candidate.json \
                --baseline eval_results_baseline.json \
                --threshold-summary-drop 0.1 \
                --threshold-dimension-floor 2.5 \
                --output comparison_report.md

          - name: Post comparison comment
            if: github.event_name == 'pull_request'
            uses: actions/github-script@v7
            with:
              script: |
                const fs = require('fs');
                const report = fs.readFileSync('comparison_report.md', 'utf8');
                github.rest.issues.createComment({
                  issue_number: context.issue.number,
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  body: report,
                });

          - name: Upload eval results
            uses: actions/upload-artifact@v4
            with:
              name: eval-results
              path: |
                eval_results_candidate.json
                eval_results_baseline.json
                eval_store.sqlite
