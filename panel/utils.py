import requests
from django.core.cache import cache
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

AVATAR_TTL = 60 * 60 * 24 * 7 # 7 days

def obtener_avatares_api() -> list:
    """ Funcion para obtener los 
    primeros 10 avatares de la API"""
    avatares = []
    seeds = ['aPSQgmwFmM', 'tXUhnGcszm', 'xQGUNihH2H', 'obiccBW1aM', 'd1aWXQ9SsK', 'KXaZ4TtGBW', 'bDzuuX34mv', 'pnRfjTolXs', '1p6JFxDnfN', '71LiTiWhLO']
    for seed in seeds:
        avatar = obtener_avatar_api(seed)
        if avatar:
            avatares.append(avatar)
    return avatares


def obtener_avatar_api(seed:str) -> str:
    """ Funcion para obtener un avatar 
    de la API dado un nombre de usuario"""
    URL = f"https://api.dicebear.com/9.x/pixel-art/svg?seed={seed}"
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException:
        return None
    
def generar_seed_aleatorio() -> str:
    """ Funcion para generar un seed aleatorio
    para la API de avatares"""
    import random
    import string
    longitud = 10
    caracteres = string.ascii_letters + string.digits
    seed = ''.join(random.choice(caracteres) for _ in range(longitud))
    return seed

def guardar_avatares_cache():
    """ Funcion para guardar los avatares en cache"""
    avatares = obtener_avatares_api()
    if avatares:
        cache.set('avatares', avatares, AVATAR_TTL)
    return avatares

def obtener_avatares_cache() -> list:
    """ Funcion para obtener los avatares de la cache"""
    avatares = cache.get('avatares')
    if not avatares:
        avatares = guardar_avatares_cache()
    return avatares


def enviarCorreo(nombreDestinatario:str,emailDestinatario:str,token:str) -> None:
    """Funcion para enviar token al correo del usuario"""
    textoPlano = f"""Hola {nombreDestinatario}, este es el token solicitado. Saludos CuestionarioAI."""
    textoHtml = f"""
    <html>
        <body>
            <h2>Hola {nombreDestinatario}, este es el token solicitado. Saludos CuestionarioAI.</h2>
            <h3 style="font-weight:bold;">{token}</h3>        
        </body>
    </html>"""

    enviado_por = 'josefbueno@gmx.es'
    password = 'Jose987456.'
    to = emailDestinatario

    mensaje = MIMEMultipart()
    mensaje['From'] = enviado_por
    mensaje['To'] = to
    mensaje['Subject'] = f'Correo para {nombreDestinatario}'  

    mensaje.attach(MIMEText(textoPlano,'plain'))
    mensaje.attach(MIMEText(textoHtml,'html'))

    # archivos = ["documento.pdf","foto.png"]

    # for archivo in archivos:
    #     with open(archivo,'rb') as fichero:
    #         mime_base = MIMEBase('application','octet-stream')
    #         mime_base.set_payload(fichero.read())
    #         encoders.encode_base64(mime_base)
    #         mime_base.add_header('Content-Disposition',f'attachment; filename={archivo}')
    #         mensaje.attach(mime_base)

    try:
        servidor = smtplib.SMTP('mail.gmx.es',587)
        servidor.starttls()
        servidor.login(enviado_por,password)
        servidor.sendmail(enviado_por,to,mensaje.as_string())
        servidor.quit()
        print("Correo enviado con exito!")
    except Exception as error:
        print(f"Error al enviar el corre: {error}")

# enviarCorreo("Jose","buenojosefrancisco@gmail.com","12345678")