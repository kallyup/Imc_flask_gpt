from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KAY")
openai.api_key = "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"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    imc = None
    nivel_obesidade = None
    genero = "femenino"
    if request.method == "POST":
        altura = float(request.form["altura"])
        peso = float(request.form["peso"])
        genero = request.form["genero"]

        # Calculando o IMC
        imc = peso / (altura ** 2)

        # Determinando o nível de obesidade
        if genero == "masculino":
            if imc < 20.7:
                nivel_obesidade = "Abaixo do Peso"
            elif 20.7 <= imc < 26.4:
                nivel_obesidade = "Peso Normal"
            elif 26.4 <= imc < 27.8:
                nivel_obesidade = "Sobrepeso"
            elif 27.8 <= imc < 31.1:
                nivel_obesidade = "Obresidade Grau I"
            else:
                nivel_obesidade = "Obesidade Grau II"
        else:
            if imc < 19.1:
                nivel_obesidade = "Abaixo do Peso"
            elif 19.1 <= imc < 25.8:
                nivel_obesidade = "Peso Normal"
            elif 25.8 <= imc < 27.3:
                nivel_obesidade = "Sobrepeso"
            elif 27.3 <= imc < 32.3:
                nivel_obesidade = "Obresidade Grau I"
            else:
                nivel_obesidade = "Obesidade Grau II"

    dieta = indica_dieta(genero,imc)
    dieta_formatado = dieta.replace("Café da manhã", '<br><strong>Café da manhã</strong>')
    dieta_formatado = dieta.replace("Almoço:", '<br><strong>Almoço:</strong>')
    dieta_formatado = dieta_formatado.replace("Janta:", '<br><strong>Janta:</strong>')
    return render_template("index.html", imc=imc, nivel_obesidade=nivel_obesidade, dieta=dieta_formatado)

def resposta(pergunta):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"responda a seguinte pergunta:{pergunta}",
        temperature=0.9,
        max_tokens=2048,
        n=1,
        stop=None
    )
    return response['choices'][0]['text'].strip()

def indica_dieta(genero, imc):
    pergunta = "faça uma pergunta"
    if (genero == "feminino" and (imc >= 25.8 )) or (genero == "masculino" and (imc >= 26.4)):
            pergunta = "diga 3 opções de reitas para café da manhã, almoço e janta para perder peso "
    elif (genero == "feminino" and (imc < 19.1)) or (genero == "masculino" and (imc < 20.7)):
            pergunta = "diga 3 opções de reitas para café da manhã, almoço e janta para ganhar massa muscular  "
    elif (genero == "feminino" and (19.1 <= imc < 25.8)) or (genero == "masculino" and (20.7 <= imc < 26.4)):
            pergunta= "o que posso fazer para manter meu peso ideal"
    '''elif genero == "masculino" and (20.7 <= imc < 26.4):
            pergunta= "o que posso fazer para manter meu peso ideal"
            
        elif genero == "masculino" and (imc < 20.7):
            pergunta = "diga 3 opções de reitas para café da manhã, almoço e janta para ganhar massa muscular  "
            
            elif genero == "masculino" and (imc >= 26.4):
            pergunta = "diga 3 opções de reitas para café da manhã, almoço e janta para perder peso  "
            '''
    
            
    respostas= resposta(pergunta)
    print(genero)
    print(pergunta)
    print(imc)
    return respostas

if __name__ == "__main__":
    app.run(debug=True)
