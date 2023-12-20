#!/usr/bin/env python3

import aws_cdk as cdk

from rafaelpombo_chatbot.rafaelpombo_chatbot_stack import RafaelpomboChatbotStack


app = cdk.App()
RafaelpomboChatbotStack(app, "RafaelpomboChatbotStack")

app.synth()
