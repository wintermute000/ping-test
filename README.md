# ping-test

A pair of ansible play and python parse script to automate ping testing from multiple Cisco IOS devices.
It is assumed that the outputs are each device's stdout contents of ping command from ios_command native ansible module

e.g. example ansible task to ping and store results per device using jinja template for formatting

```
  - name: ping test
    ios_command:
      provider: "{{ provider }}"
      commands: ping {{ item.destination }} source {{ item.source }} repeat {{ item.repeat }} timeout {{ item.timeout }} size {{ item.size }}

    with_items: "{{ ping_targets }}"
    register: ping

  - template: src=./templates/ping.j2 dest=./show_outputs/{{ inventory_hostname }}.ping.output.txt
```

e.g. example jinja template
```
{% for p in ping.results %}
{{ p.stdout }}
{% endfor %}
```

#DEPENDENCIES
- ansible 2.1+
- python 2.x

#ANSIBLE COMPONENTS
- ping-play.yml - this ansible play runs multiple pings and places the outputs in ./show_outputs
- setuplab.yml - this ansible play sets up a sample lab environment which this repo was tested against.

#CORRECT DEFINITIONS
Define the correct ping results per device in ansible host_vars e.g.

```
ping_targets:
    - source: 4.4.4.4
      destination: 1.1.1.1
      repeat: 3
      timeout: 2
      size: 1500

    - source: 4.4.4.4
      destination: 2.2.2.2
      repeat: 3
      timeout: 2
      size: 1500
```

#PYTHON COMPONENTS
- check-ping.py - checks the results of the ping tests defined in hostvars

#SAMPLE LAB
The sample lab is defined in hostvars via standard ansible YAML. It consists of 4 IOS routers in a ring. 
Lab topology is provided as a png file in the repo.
r4 is intentionally missing the configurations for Loopback88 (88.88.88.88/32) and the corresponding OSPF network statements.
This has the following consequences:
- The interface Lo88 will come up as missing
- pings to 88.88.88.88 fails

#USAGE
- call ansible playbook ping-play.yml
- run ping-test.py with appropriate variables defined

#EXAMPLE: HOW TO USE
```
    correct_path = "./host_vars"

    host_path = "./host_vars"
    host_file = "hosts.yml"
    show_path = "./show_outputs"

    ping_filename = "ping.output.txt"

    job = ping_test()
    hosts = job.generate_host_list(host_path,host_file)
    check_pings = job.parse_pings(hosts, show_path, ping_filename)
```

#EXAMPLE OUTPUTS
- example-ping-play.txt - shows output of ansible ping tasks
- example-ping-test.txt - shows output of python parser
