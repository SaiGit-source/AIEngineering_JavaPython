import asyncio
import sys
from time import time

import gradio as gr
from sidekick import Sidekick
from fastapi.responses import HTMLResponse
import time as system_time


# FIX FOR WINDOWS: Prevents asynchronous subprocess pipe collisions
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


def get_new_agent():
    """Instantiates a clean, unbaked Sidekick object instantly without blocking."""
    print("🤖 New Sidekick session container allocated.")
    return Sidekick()

#async def setup():
#    sidekick = Sidekick()
#    await sidekick.setup()
#    return sidekick


async def handle_ui_logout(sidekick_agent):
    """Explicit wrapper to clear background resources immediately when the logout button is clicked."""
    print("🚪 Logout button clicked. Terminating background threads...")
    if sidekick_agent:
        try:
            await sidekick_agent.logout()
            print("✅ Sidekick background logout completed successfully.")
        except Exception as e:
            print(f"Exception during custom logout cleanup: {e}")
            
    # CRITICAL FIX: Explicitly return None to clear the gr.State object in the UI
    return None


async def process_message(sidekick_agent, message, success_criteria, history, request: gr.Request):
    # Fallback Guard: If the state is somehow missing, generate an instance instantly
    active_agent = sidekick_agent if sidekick_agent is not None else Sidekick()
    
    # 1. Extract the logged-in username
    username = request.username if (request and request.username) else "default_user"
    print(f"👤 Message received from user: {username}")

    # LAZY INITIALIZATION: Check if tools are configured yet. If not, spin them up here.
    if active_agent.worker_llm_with_tools is None:
        print("🔧 Lazy-initializing browser tools and LangGraph structure...")
        try:
            await active_agent.setup()
            print("✅ Browser engines and agent nodes successfully configured!")
        except Exception as setup_error:
            print("❌ CRITICAL: Browser tools configuration failed inside execution thread!")
            import traceback
            traceback.print_exc()
            
            error_card = {
                "role": "assistant",
                "content": f"❌ **Execution Crash**: Failed to start browser drivers.\n\n```text\n{str(setup_error)}\n```"
            }
            if isinstance(history, list):
                history.append(error_card)
            else:
                history = [error_card]
            return history, active_agent

    # Execute the core agent loop superstep sequence
    print(f"⚡ Processing superstep request: {message}")
    results = await active_agent.run_superstep(message, success_criteria, history, thread_id=username)
    return results, active_agent

#async def process_message(sidekick, message, success_criteria, history):
#    results = await sidekick.run_superstep(message, success_criteria, history)
#    return results, sidekick


async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, new_sidekick


def free_resources(sidekick):
    print("Cleaning up")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick Personal Co-Worker")
    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Sidekick")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success critiera?"
            )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")
        logout_button = gr.Button("Log Out", variant="secondary")

    #ui.load(setup, [], [sidekick]) # creates new instance of sidekick on load and stores it in state
    #     sidekick = Sidekick()
    message.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])
    
    # CLEAN LOGOUT STEP 2: Clear browser storage and drop cookies by redirecting to the absolute logout page
    logout_button.click(
        fn=None,
        inputs=None,
        outputs=None,
        js="() => { window.location.replace('/logout'); }"
    )
    
    
    # Triggers your async background engine cleanup and reloads the interface cleanly
    logout_button.click(handle_ui_logout, [sidekick], [sidekick]).then(
        fn=None, js="() => { window.location.href = '/logout'; }"
    )


# --- ROUTE INJECTION FOR FASTAPI AUTH DESTRUCTION (OUTSIDE BLOCKS) ---
# if __name__ == "__main__":
#     # Initialize the Gradio interface layout framework first
#     app, local_url, share_url = ui.queue().launch(
#         inbrowser=True, 
#         auth=[("admin", "secret123"), ("saito", "agentic2026")],
#         prevent_thread_lock=True # Allows code beneath to continue executing
#     )

#     # Access Gradio's underlying FastAPI server instance
#     fastapi_server = ui.app

#     @fastapi_server.get("/explicit_logout")
#     async def explicit_logout():
#         """Accepts the fake credentials to overwrite the browser's authentication cache."""
#         # Returning 200 instead of 401 prevents the browser from locking up the login fields
#         return HTMLResponse(content="<body>Session cleared.</body>", status_code=200)

#     # Keep the main process running smoothly
#     try:
#         while True:
#             system_time.sleep(1)
#     except KeyboardInterrupt:
#         print("Stopping application server container.")

## This also works!!!!
# ui.launch(inbrowser=True)
# ##Pass a list of authorized user credentials
# ui.launch(
#    inbrowser=True, 
#    auth=[("admin", "secret123"), ("saito", "agentic2026")]
# )


# --- NATIVE APPLICATION ENTRY POINT ---
if __name__ == "__main__":
    # Gradio handles authentication sessions and provides a native /logout endpoint out of the box
    ui.queue().launch(
        inbrowser=True, 
        auth=[("admin", "secret123"), ("saito", "agentic2026")],
        auth_message="Please enter your Sidekick Co-Worker credentials."
    )