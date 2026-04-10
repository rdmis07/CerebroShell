import glfw
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer
import subprocess

from llm import nlp_to_shell_command,Query

def execute_command(cmd):
    try:
        if isinstance(cmd, str):

            cmd = cmd.replace('"', '\\"') 
            cmd = f'cmd /c "{cmd}"'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        return "", str(e)


def main():
    if not glfw.init():
        print("Could not initialize GLFW")
        return

    width, height = 800, 600
    window = glfw.create_window(width, height, "CerebroShell Terminal", None, None)
    glfw.make_context_current(window)

    imgui.create_context()
    io = imgui.get_io()

    io.font_global_scale = 1
    monospace_font_path = "C:/Windows/Fonts/consola.ttf"
    font_size = 27
    io.fonts.add_font_from_file_ttf(monospace_font_path, font_size)

    impl = GlfwRenderer(window)

    # Terminal state
    command_input = ""
    output_lines=[]
    output_lines = ["🧠 Welcome to your NLP Terminal"]
    command_history = []
    scroll_to_bottom = True

    # Colors
    # color_stdout = (0.85, 0.85, 0.85)   # soft white/gray
    # color_stderr = (1.0, 0.3, 0.3)      # bright red for errors
    # color_prompt = (0.3, 0.7, 1.0)      # light blue/cyan accent
    # background_color = (0.1, 0.1, 0.1)  # very dark gray

    background_color = (0.03, 0.03, 0.03)      # pure dark base

    color_stdout  = (0.90, 0.90, 0.90)         # bright white
    color_prompt  = (0.20, 0.80, 0.40)         # bright neon green
    color_stderr  = (1.00, 0.20, 0.20)         # strong, pure red




    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        # Style
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (2, 2))

        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(width, height)
        flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE
        imgui.begin("Terminal", True, flags=flags)

        # Single child: all output + input inline
        if imgui.begin_child("terminal_output", width, height, border=True,
                            ):
            imgui.push_text_wrap_pos(width)
            for line in output_lines[-100000:]:
                if line.startswith("[ERROR]"):
                    imgui.text_colored(line, *color_stderr)
                elif line.startswith(">"):
                    imgui.text_colored(line, *color_prompt)
                else:
                    imgui.text_colored(line, *color_stdout)
            if scroll_to_bottom:
                imgui.set_scroll_here_y(1.0)  # scrolls to bottom
                scroll_to_bottom = False
            # Input inline at last line
            imgui.text_colored("prash > ", *color_prompt)
            imgui.same_line()

            # Make input background transparent
            imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *background_color, 1.0)
            imgui.push_style_color(imgui.COLOR_TEXT_SELECTED_BACKGROUND, *background_color, 1.0)

            changed, command_input = imgui.input_text(
                "##inline_input",
                command_input,
                512,
                imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
            )
            imgui.set_keyboard_focus_here()
            imgui.pop_style_color(2)

            if changed and command_input.strip():
                # Save history
                # command_history.append(command_input)
                # Append prompt + command to output

                output_lines.append(f"prash > {command_input}")
                
                if io.key_shift:
                    command_input=nlp_to_shell_command(command_input)
                    output_lines.append(f"Command: {command_input}")
                    ctr=command_input
                    # output_lines.append("wanna execute it y/n")
                    # if io.keys_down[imgui.KEY_Y, False]:   # <-- short and correct
                    # stdout, stderr = execute_command(command_input)
                    # output_lines.append("dahlfh")
                # Execute command
                if io.key_ctrl:
                    response=Query(command_input)
                    output_lines.append(response)
                    ctr=None
                else:
                    ctr=command_input
                if ctr:
                    stdout, stderr = execute_command(command_input)
                    for line in stdout.splitlines():
                        output_lines.append(line)
                    for line in stderr.splitlines():
                        output_lines.append(f"[ERROR] {line}")
                    command_input = ""
                    scroll_to_bottom = True

            # Scroll to bottom
            if scroll_to_bottom:
                imgui.set_scroll_here_y()
                scroll_to_bottom = True

            imgui.end_child()

        imgui.end()
        imgui.pop_style_var(2)

        # Render
        glClearColor(*background_color, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()
