from .llm import LLM
from .models import (
    LiveCodeRequest,
    LiveCodeResult,
)
from .prompt_templates.assistant import (
    livecoder_system,
    livecoder_prompt_template,
)


class LiveCoder:
    def __init__(self):
        self.livecoder_params = {"temperature": 0.7, "max_tokens": 500}
        self.livecoder_system = livecoder_system.template

        self.livecoder = LLM(
            system_message=self.livecoder_system,
            params=self.livecoder_params,
        )

        self.orbits = ["d1", "d2", "d3"]  # , "d4"]
        self.orbit_idx = 0

    def __call__(
        self,
        message,
        session_id=None,
    ) -> LiveCodeResult:
        if session_id and session_id not in self.livecoder.sessions:
            self.livecoder.new_session(
                id=session_id,
                system=self.livecoder_system,
                params=self.livecoder_params,
            )

        orbit = self.orbits[self.orbit_idx]
        self.orbit_idx = (self.orbit_idx + 1) % len(self.orbits)

        input_prompt = livecoder_prompt_template.substitute(
            request=message,
            orbit=orbit,
        )

        print("input_prompt:", input_prompt)

        output = self.livecoder(
            input_prompt,
            id=session_id,
            output_schema=LiveCodeResult,
            model="gpt-4-1106-preview",
        )

        # strip ending newline characters
        while output["code"][-1] == "\n":
            output["code"] = output.code[:-1]

        return output
