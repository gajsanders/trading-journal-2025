from jinja2 import Template

METRICS_TEMPLATE = Template('''
## Key Metrics Overview
- **Win Rate:** {{ win_rate }}
- **Total PnL:** {{ total_pnl }}
- **Time-Weighted Return:** {{ time_weighted_return }}
- **Risk-Adjusted Return:** {{ risk_adjusted_return }}
''')

CHARTS_TEMPLATE = Template('''
## Visual Section
{{ charts_md | safe }}
''')

INSIGHTS_TEMPLATE = Template('''
## Detailed Analysis Section
{{ insights }}
''')

REFLECTION_TEMPLATE = Template('''
## Monthly Reflection Questions
{% for q in questions %}- {{ q }}
{% endfor %}
''')

ACTIONS_TEMPLATE = Template('''
## Action Items and Improvement Areas
{% for item in action_items %}- {{ item }}
{% endfor %}
''') 