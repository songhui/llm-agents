from autogen import ConversableAgent

def second_last_msg(sender: ConversableAgent, recipient: ConversableAgent, summary_args: dict):
    return sender.chat_messages[recipient][-2]["content"]