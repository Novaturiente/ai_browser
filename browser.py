from google import genai
from google.genai import types
import test_tools as agent_tools 

# Initialize Gemini API client and configuration
client = genai.Client()
tool_map = agent_tools.tool_map
gemini_tools = types.Tool(function_declarations=agent_tools.tool_list)  # pyright: ignore
config = types.GenerateContentConfig(
    tools=[gemini_tools],
    system_instruction="""You are an AI assistant who helps the user to browse webpages and take actions in webpages.
    The webpage information will be given as source of the webpage inspect the source then use the available tools to navigate through webpages and take necessary actions. 
    If the user does not specify any url try to figure out which website or url to use, if not able to figure out you can use Duckuckgo search to do websearch.

    'Always use full XPATH location of the element when navigating webpages, do not use shortened version of the xpath'
    """,
)

with open("test.html", "r") as f:
    html_source = f.read()

# Initial state variables for the chat
messages = [
    {
        "role": "user",
        "content": "Which is the latest mkbhd video in youtube",
    }
]


i = 1
last_error = ""
latest_source = agent_tools.latest_source

while True:
    try:
        # Send request with function declarations
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{messages}\n\nLatest source:{latest_source}",
            config=config,
        )

        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:  # pyright: ignore
            function_call = response.candidates[0].content.parts[0].function_call  # pyright: ignore
            name = function_call.name
            arguments = function_call.args
            print(function_call)
            messages.append({"role": "assistant", "contnet": f"{function_call}"})

            function_to_run = tool_map.get(f"{name}")
            if function_to_run:
                message = function_to_run(**arguments) # pyright: ignore
                messages.append({"role": "user", "content": message})
            else:
                f"{name} not in tools"
        else:
            print(response.text)
            break
    except Exception as e:
        if last_error == str(e):
            i += 1
        print(f"{i} : {e}")
        if i == 3:
            break
        last_error = str(e)
