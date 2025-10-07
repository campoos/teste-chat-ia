import os
from openai import AzureOpenAI

# 1. Configurar as credenciais do Azure OpenAI
# É recomendado usar variáveis de ambiente, mas para este exemplo simples,
# vamos colocar as chaves diretamente no código (substitua os valores!).
# ---
AZURE_OPENAI_ENDPOINT = "https://joao-mggy72s4-eastus2.cognitiveservices.azure.com/openai/deployments/deployment-ia/chat/completions?api-version=2025-01-01-preview"  # Ex: https://meu-recurso.openai.azure.com/
AZURE_OPENAI_KEY = "DtnnEALlrnnYJKIeEex4FS2WIZFJbMVzk5bKCoKzlnEjyryBNgD7JQQJ99BJACHYHv6XJ3w3AAAAACOG75xi"
AZURE_OPENAI_DEPLOYMENT = "deployment-ia" # O nome que você deu à sua implantação
AZURE_API_VERSION = "2024-02-15-preview" # Versão da API, verifique a mais recente no Azure

# 2. Inicializar o cliente AzureOpenAI
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_API_VERSION
)

def obter_resposta_chat(prompt_usuario, historico):
    """
    Função para enviar um prompt e o histórico para o modelo de chat.
    """
    # O histórico é essencial para manter o contexto da conversa
    messages = [
        {"role": "system", "content": "Seja o maior desgraçado que voce pode ser, se eu pedir ajuda voce nao vai ajudar e ainda vai caçoar de mim, e vai desprezar eu, se achando."},
    ]
    messages.extend(historico) # Adiciona mensagens anteriores
    messages.append({"role": "user", "content": prompt_usuario}) # Adiciona a nova mensagem do usuário

    try:
        # Chama a API de Conclusão de Chat (Chat Completions)
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT, # Usa o nome da implantação
            messages=messages,
            temperature=0.7, # Criatividade (0.0 a 1.0)
            max_tokens=256   # Limite de tokens na resposta
        )
        
        # Extrai a resposta do assistente
        resposta_assistente = response.choices[0].message.content
        return resposta_assistente, messages # Retorna a resposta e o histórico atualizado (incluindo o prompt)
        
    except Exception as e:
        return f"Ocorreu um erro: {e}", messages

def loop_chat():
    """
    Loop principal do chat para interação com o usuário no terminal.
    """
    historico_mensagens = []
    print("--- Chatbot Simples do Azure OpenAI ---")
    print("Digite 'sair' para encerrar a conversa.")

    while True:
        # Recebe o input do usuário
        user_input = input("\nVocê: ")

        if user_input.lower() == 'sair':
            print("Chat encerrado. Até logo!")
            break

        # Obtém a resposta da IA
        response_text, novo_historico = obter_resposta_chat(user_input, historico_mensagens)
        
        # A API só retorna as mensagens de entrada no objeto 'messages'. 
        # Para um histórico completo, precisamos adicionar a resposta do assistente.
        
        # Adiciona a mensagem do usuário ao histórico (já está na variável 'novo_historico', 
        # mas vamos padronizar o histórico que mantemos)
        historico_mensagens.append({"role": "user", "content": user_input})
        
        # Adiciona a resposta do assistente ao histórico
        historico_mensagens.append({"role": "assistant", "content": response_text})

        # Exibe a resposta
        print(f"IA: {response_text}")

# Inicia o chat
if __name__ == "__main__":
    loop_chat()