from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)


class LLMService:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            model_name = (
                "Qwen/Qwen2.5-3B-Instruct"
            )

            tokenizer = (
                AutoTokenizer.from_pretrained(
                    model_name
                )
            )

            model = (
                AutoModelForCausalLM.from_pretrained(
                    model_name,
                    device_map="auto"
                )
            )

            cls._instance.pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer
            )

        return cls._instance

    def generate(
        self,
        prompt,
        max_tokens=1500
    ):

        result = self.pipe(
            prompt,
            max_new_tokens=max_tokens,
            temperature=0.4,
            do_sample=True
        )

        return result[0]["generated_text"]