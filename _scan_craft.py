import re, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blocks_dir = r'pipeline\translate\软件工程匠艺\blocks'

# Minimal whitelist: acronyms, tech terms, proper names commonly kept in English
wl = set()
wl |= set('api apis cpu gpu ram ssd html css json xml yaml http https tcp udp ip dns tls ssl ssh url uuid sql crud acid cap git ci cd pr tdd bdd ddd fp oop dry kiss yagni solid mvp mvc cli gui ide sdk jvm gc aws gcp azure docker k8s helm nginx redis kafka jenkins github gitlab react vue angular node npm yarn pip java kotlin scala python ruby go rust swift typescript javascript linux unix macos windows rest grpc graphql rpc oauth jwt saas paas iaas ai ml dl nlp llm gpt bert cnn rnn lstm pdf csv yaml toml i18n l10n a11y utf ascii unicode eof gui tui roi kpi okr agile scrum kanban xp lean sonar junit mockito selenium cypress playwright jmeter gatling prometheus grafana elasticsearch logstash kibana jaeger zipkin datadog terraform ansible consul vagrant argocd istio envoy hystrix mybatis spring boot quarkus django flask fastapi rails express koa nestjs mysql postgres sqlite mongodb cassandra dynamodb hbase neo4j tidb clickhouse spark flink hadoop hive airflow dbt tensorflow pytorch jax keras huggingface langchain openai anthropic svm knn kmeans pca xgboost gan vae mdp dqn ppo csrf xss ssrf rce sqli waf ids ips siem mfa sso saml oidc pki ca crl ocsp x509 pem der hsts csp cors sast dast iaast rasp sca cve nvd cwe owasp slo sla sli mttr mtbf rca rto rpo ha dr bcp'.split())
wl |= set('bob martin fowler beck cunningham gamma knuth dijkstra hoare lamport parnas brooks nygard ford hickey carmack spolsky kent hunt thomas feathers evans vernon nystrom metz pragmatic gang four gof'.split())
wl |= set('true false null none nil void int float double bool char byte short long string str list dict set tuple array vector matrix map queue stack heap tree graph node edge dfs bfs dp np logn p50 p90 p99 rps qps tps'.split())
wl |= set('id ip mac os vm lan wan vpn nas raid ext ntfs fat smtp pop imap ldap snmp ntp ssh telnet ssl dtls aes des rsa ecdsa ed25519 sha hmac md5 blake'.split())
wl |= set('wip todo fixme rfc iso ieee acm w3c ecma gpl mit apache bsd mpl lgpl wcag'.split())

files = sorted(glob.glob(os.path.join(blocks_dir, '*.md')))
issues = {}
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    in_code = False
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        clean = re.sub(r'`[^`]*`', '', line)
        clean = re.sub(r'（[A-Za-z\s\-\.]+）', '', clean)
        clean = re.sub(r'\([A-Za-z\s\-\.]+\)', '', clean)
        clean = re.sub(r'https?://\S+', '', clean)
        clean = re.sub(r'<[^>]+>', '', clean)
        for m in re.finditer(r'[\u4e00-\u9fff]\s*([a-zA-Z]{3,})\s*[\u4e00-\u9fff]', clean):
            w = m.group(1).lower()
            if w not in wl:
                issues.setdefault(w, []).append((os.path.basename(fp), i+1, s[:100]))
        for m in re.finditer(r'([a-zA-Z]{3,})\s*[\u4e00-\u9fff]', clean):
            w = m.group(1).lower()
            if w not in wl:
                issues.setdefault(w, []).append((os.path.basename(fp), i+1, s[:100]))
        for m in re.finditer(r'[\u4e00-\u9fff]\s*([a-zA-Z]{3,})', clean):
            w = m.group(1).lower()
            if w not in wl:
                issues.setdefault(w, []).append((os.path.basename(fp), i+1, s[:100]))

sorted_items = sorted(issues.items(), key=lambda x: -len(x[1]))
print(f'=== 软件工程匠艺: {len(sorted_items)} unique English words embedded in Chinese prose ===')
for word, occs in sorted_items:
    print(f'  {word} ({len(occs)}x): {occs[0][0]}:{occs[0][1]} {occs[0][2]}')
