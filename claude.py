import anthropic
import re

ANTHROPIC_API_KEY = "" # Put your API key here!
DEFAULT_MODEL = "claude-3-haiku-20240307"

CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def extract_structure(response):
    # Find the first occurrence of '[' and '{'
    first_square_bracket = response.find('[')
    first_curly_bracket = response.find('{')

    # Determine which comes first
    if first_square_bracket != -1 and (first_curly_bracket == -1 or first_square_bracket < first_curly_bracket):
        # '[' comes first
        start_index = first_square_bracket
        end_index = response.rindex(']') + 1
    elif first_curly_bracket != -1:
        # '{' comes first
        start_index = first_curly_bracket
        end_index = response.rindex('}') + 1
    else:
        # Neither '[' nor '{' found
        return response

    return response[start_index:end_index]

def escape_safe_json(json_str):
    json_str = re.sub(r'\s*(\{|\}|\[|\])\s*', r'\1', json_str) ## remove whitespace around brackets and colons
    json_str = re.sub(r'(":\s*\d+)\s*,\s*', r'\1,', json_str) ## remove whitespace after numbers ":123,
    json_str = re.sub(r'("|]|}),\s+"', r'\1,"', json_str) ## remove whitespace after delimiting commas
    # json_str = re.sub(r'(?<=[{\[",])\s*([^"]\w+)\s*:', r'"\1":', json_str) ## add quotes to keys

    # # Regex to operate ONLY within string values
    pattern = re.compile(r'("\s*:\s*"|\[\s*"|"\s*,\s*")(.*?)(?="\s*(,"|}|]|,\[|,{))', re.DOTALL)
    # ((?:[^"\\]|\\.)*?) -- this is originally escaped content

    # Function to replace double quotes within the string value
    def escape_quotes(match):
        avoid_keys = re.compile(r'"\s*:\s*({"|\["|")')
        start_index = avoid_keys.search(match.group(2))
        if not start_index:
            escaped_content = match.group(2).replace('\\"', '"').replace('"', '\\"')
        else:
            start_index = start_index.end()
            escaped_content = match.group(2)[:start_index]+match.group(2)[start_index:].replace('\\"', '"').replace('"', '\\"')
        # print(match.group(1)+"_____________"+escaped_content)
        return match.group(1) + escaped_content
    
    escaped_json = pattern.sub(escape_quotes, json_str).replace('\n', '\\n').replace('\t', '\\t').replace('\b', '\\b')
    return escaped_json

def prompt(prompt, model=DEFAULT_MODEL):
    message = CLIENT.messages.create(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content":  prompt
            }
        ],
        temperature=0
    ).content[0].text
    message = extract_structure(message)
    message = escape_safe_json(message)
    return message