import functions_framework
from vertexai.generative_models import GenerativeModel

@functions_framework.http
def summarize(request):
    # return "Hello", 200

    request_json = request.get_json(silent=True)
    url = request_json.get("url") if request_json else None
    if not url:
        return "Please provide a URL in JSON body: {\"url\": \"https://example.com\"}", 400

    model = GenerativeModel("gemini-2.0-flash-001")
    response = model.generate_content(f'summarize {url}',generation_config={"max_output_tokens": 120})
    return response.text,200
