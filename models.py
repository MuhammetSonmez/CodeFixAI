import traceback
import re
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class CodeFixAI:
    def __init__(self, model_version: str, model_name: str) -> None:
        self.model = OllamaLLM(model=model_version, name=model_name)

    def debug(self, lang: str, code: str) -> str:
        run_result = self.run_code(user_code=code)
        debug_text = self.debug_code(lang=lang, code=run_result["code"], output=run_result["output"], error=run_result["error"])
        return self.extract_code_blocks(debug_text)

    def debug_code(self, lang: str, code: str, output: str, error: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "Fix this {lang} code and give me the all solution:\n{code}\nOutput: {output}\nError: {error}"
        ).format(lang=lang, code=code, output=output, error=error)
        return self.model.invoke(prompt)

    def run_code(self, user_code: str) -> dict:
        local_env = {}
        try:
            exec(user_code, {}, local_env)
            return {"output": local_env, "error": None, "code": user_code}
        except Exception:
            return {"output": None, "error": traceback.format_exc(), "code": user_code}

    def extract_code_blocks(self, text: str) -> str:
        code_blocks = re.findall(r'```(?:python)?\n(.*?)```|"""(?:python)?\n(.*?)"""', text, re.DOTALL)[0]
        extracted_code = [code for code in code_blocks if code]
        return "\n\n".join(extracted_code)

model = CodeFixAI(model_version="llama3.2", model_name="debugger")
