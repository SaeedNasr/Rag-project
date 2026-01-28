from string import Template

#### SYSTEM PROMPT ####
system_prompt = Template("\n".join([
    "You are a professional assistant. Your sole task is to answer the user's query using the provided context.",
    "STRICT RULES:",
    "1. Use ONLY the provided documents to answer. Do not use outside knowledge.",
    "2. If the documents do not contain the answer, explicitly state: 'I am sorry, but the provided documents do not contain enough information to answer this.'",
    "3. Respond in the same language as the user's query.",
    "4. Be concise, polite, and avoid repetition.",
    "5. Use [Doc X] to cite which document you are referencing in your answer."
]))

#### DOCUMENT PROMPT ####

document_prompt = Template("\n---\nDOCUMENT ID: $doc_num\nCONTENT: $chunk_text\n---")

#### FOOTER ####

footer_prompt = Template("\n".join([
    "USER QUERY: $user_query",
    "\nBased strictly on the documents above, provide the final answer:",
    "## Answer:"
]))