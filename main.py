import yaml
import requests
from yaml import Loader


def load_rules_set(name):
    with open(name) as stream:
        objs = yaml.load_all(stream, Loader)
        providers, rules = objs
        return providers["rule-providers"], rules["rules"]


def add_general(f):
    with open("general.txt") as g:
        f.write(g.read())


def add_domain_rule(f, objs, policy):
    domain = filter(lambda x: not x.startswith("+."), objs)
    domain_suffix = filter(lambda x: x.startswith("+."), objs)
    for d in domain:
        f.write(f"DOMAIN,{d},{policy}\n")
    for d in domain_suffix:
        f.write(f"DOMAIN-SUFFIX,{d[2:]},{policy}\n")


def add_ip_rule(f, objs, policy):
    ipv4 = filter(lambda x: "." in x, objs)
    ipv6 = filter(lambda x: ":" in x, objs)
    for ip in ipv4:
        f.write(f"IP-CIDR,{ip},{policy}\n")
    for ip in ipv6:
        f.write(f"IP-CIDR6,{ip},{policy}\n")


def add_rule_set(f, provider, policy):
    url = provider["url"]
    behavior = provider["behavior"]
    resp = requests.get(url)
    st = yaml.load(resp.text, Loader)
    payload = st["payload"]
    if behavior == "domain":
        add_domain_rule(f, payload, policy)
    elif behavior == "ipcidr":
        add_ip_rule(f, payload, policy)


def add_rules(f, providers, rules):
    f.write("[Rule]\n")
    final_rule = None
    for rule in rules:
        itmes = rule.split(",")
        # type, [obj,] policy
        typ = itmes[0]
        if typ == "MATCH":
            final_rule = itmes[1]
            continue
        if typ == "GEOIP":
            f.write(f"{rule}\n")
            continue
        if typ == "RULE-SET":
            provider, policy = itmes[1:]
            add_rule_set(f, providers[provider], policy)

    final_rule = final_rule or "DIRECT"
    f.write(f"FINAL,{final_rule}\n")


def main():
    providers, rules = load_rules_set("rules-set.yaml")
    with open("sr_rule.conf", "w") as f:
        add_general(f)
        add_rules(f, providers, rules)


if __name__ == "__main__":
    main()
