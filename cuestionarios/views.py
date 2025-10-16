from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse,HttpResponse
from django.db.models import Count
from .models import *
from authentication.models import Usuarios
from .utils import *
import math
import json
# Create your views here.

class CuestionariosView(View):

    def get(self,request,n_pagina=1):
        # user_request = Usuarios.objects.get(username=request.user)
        # print("USER REQUEST: ",user_request)
        busqueda = request.GET.get('busqueda', '')
        tema = request.GET.get('tema','')
        filtros = request.GET.get('filtros','')
        if busqueda != "":
            n_pagina = 1
        #El numero de pagina se utilizara para seleccionar los cuestionario atraves de 
        #una especie de indicie, una pagina tiene 8 cuestionarios y si es la pagina 1
        #se mostraran los primero 8 cuestionario y asi sucesivamente
        indice = n_pagina * 8
        desde = indice - 8
        cuestionarios_mostrar = []
        if filtros:
            if tema != "" and busqueda == "":
                cuestionarios = Cuestionarios.objects.annotate(
                    num_preguntas=Count('preguntas',distinct=True),
                    num_respuestas=Count('preguntas__respuestas',distinct=True)
                    ).select_related('id_tema_fk').filter(id_tema_fk=tema)
                cuestionarios_mostrar = cuestionarios[desde:indice]
            elif tema != "" and busqueda == "":
                cuestionarios = Cuestionarios.objects.annotate(
                    num_preguntas=Count('preguntas',distinct=True),
                    num_respuestas=Count('preguntas__respuestas',distinct=True)
                    ).select_related('id_tema_fk').filter(id_tema_fk=tema)
                cuestionarios_mostrar = cuestionarios[desde:indice]
            elif tema != "" and busqueda != "":
                cuestionarios = Cuestionarios.objects.annotate(
                    num_preguntas=Count('preguntas',distinct=True),
                    num_respuestas=Count('preguntas__respuestas',distinct=True)
                    ).select_related('id_tema_fk').filter(id_tema_fk=tema,nombre_cuestionario__icontains=busqueda)
                cuestionarios_mostrar = cuestionarios[desde:indice]
            elif tema == "" and busqueda != "":
                cuestionarios = Cuestionarios.objects.annotate(
                    num_preguntas=Count('preguntas',distinct=True),
                    num_respuestas=Count('preguntas__respuestas',distinct=True)
                    ).select_related('id_tema_fk').filter(nombre_cuestionario__icontains=busqueda)
                cuestionarios_mostrar = cuestionarios[desde:indice]
            elif tema == "" and busqueda == "":
                cuestionarios_mostrar = Cuestionarios.objects.annotate(
                    num_preguntas=Count('preguntas',distinct=True),
                    num_respuestas=Count('preguntas__respuestas',distinct=True)
                    ).select_related('id_tema_fk').all()[desde:indice]
            return render(request,"cuestionarios/cuestionarios-filtros.html",{"cuestionarios":cuestionarios_mostrar})
        elif busqueda:
            cuestionarios = Cuestionarios.objects.annotate(
                num_preguntas=Count('preguntas',distinct=True),
                num_respuestas=Count('preguntas__respuestas',distinct=True)
                ).select_related('id_tema_fk').filter(nombre_cuestionario__icontains=busqueda)
        else:
            cuestionarios = Cuestionarios.objects.annotate(
                num_preguntas=Count('preguntas',distinct=True),
                num_respuestas=Count('preguntas__respuestas',distinct=True)
                ).select_related('id_tema_fk').all()
        cuestionarios_mostrar = cuestionarios[desde:indice]
        n_cuestionarios = len(cuestionarios)
        n_paginas = n_cuestionarios / 8
        n_paginas = math.ceil(n_paginas)
        numeracion = [{"indice":n,"ruta":f"/cuestionarios/{n}"} for n in range(1,n_paginas+1)]
        temas = Temas.objects.all()
        #Si la pagina es divisible entre 5 es que hay que mostrar los siguientes numeros porque
        # este en el inicio o final de los 5 indices
        if n_pagina % 5 == 0 or n_pagina == 1:
            inicio = (n_pagina - 1) // 5 * 5
            fin = inicio + 5
            numeracion = numeracion[inicio:fin]
            siguiente = n_pagina + 1 if n_pagina < n_paginas else n_pagina
            anterior = n_pagina - 1 if n_pagina > 1 else 1
        else:
            inicio = (n_pagina - 1) // 5 * 5
            fin = inicio + 5
            numeracion = numeracion[inicio:fin]
            siguiente = n_pagina + 1 if n_pagina < n_paginas else n_pagina
            anterior = n_pagina - 1 if n_pagina > 1 else 1
        return render(request,"cuestionarios/cuestionarios.html",{"cuestionarios":cuestionarios_mostrar,"indices":numeracion,
                    "siguiente":siguiente,"anterior":anterior,"temas":temas})

class CrearCuestionarioView(View):

    def get(self,request):

        temas = Temas.objects.all()

        return render(request,"cuestionarios/cuestionario.html",{"temas":temas})
    
    def post(self,request):
        try: 
            enlace = ""
            data = {}
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                enlace = data.get("enlace")
            else:
                enlace = request.POST.get("enlace")

            if enlace == "generar":
                #Obtenemos el archivo PDF enviado por el formulario
                archivo = request.FILES.get("archivo", "")
                # Obtenemos los datos enviados por el formulario
                nombre_cuestionario = request.POST["nombre"]
                tema = request.POST["tema"]
                print("TEMA DEL CUESTIONARIO: ",tema)
                preguntas = request.POST["preguntas"]
                respuestas = request.POST["respuestas"]
                # correctas = request.POST["correctas"] if request.POST["correctas"] != "" else "1"
                descripcion = request.POST["descripcion"]
                prompt = request.POST.get("prompt-cuestionarios", "")
                print("Texto prompt: "+prompt)
                enlace = request.POST["enlace"]
                if archivo != "":
                    #Obtenemos el texto del PDF y generamos el cuestionario
                    texto_pdf = extraer_texto_pdf_directo(archivo)
                    cuestionario_generado = procesar_pdf_y_generar_cuestionario_json(texto_pdf,total_preguntas=int(preguntas),
                                            n_respuestas=int(respuestas))
                elif prompt != "":
                    print("Texto prompt: "+prompt)
                    cuestionario_generado = procesar_pdf_y_generar_cuestionario_json(prompt,total_preguntas=int(preguntas),
                        n_respuestas=int(respuestas))
                # cuestionario_generado_array = [cuestionario_generado]
                id_pregunta = 0
                id_respuesta = 0
                preguntas_respuestas = []
                for pregunta in cuestionario_generado:
                    id_pregunta += 1
                    pregunta_objeto = {}
                    pregunta_objeto["pregunta"] = {"pregunta":pregunta["pregunta"],"id":id_pregunta,"respuesta_correcta":pregunta["respuesta_correcta"]}
                    respuestas = []
                    for respuesta in pregunta["opciones"]:
                        id_respuesta += 1
                        if respuesta == pregunta["opciones"][pregunta["respuesta_correcta"]]:
                            respuesta_objeto = {"respuesta":respuesta,"id":id_respuesta, "respuesta_correcta":True}
                        else:
                            respuesta_objeto = {"respuesta":respuesta,"id":id_respuesta, "respuesta_correcta":False}
                        respuestas.append(respuesta_objeto)
                    pregunta_objeto["respuestas"] = respuestas
                    preguntas_respuestas.append(pregunta_objeto)

                return render(request, "cuestionarios/cuestionario-editor.html", {"cuestionario": {"id":1,"nombre":nombre_cuestionario,"tema":tema,
                "descripcion":descripcion},"preguntas": preguntas_respuestas})
            
            elif enlace == "guardar":
                nombre_cuestionario = data.get("nombre")
                tema = data.get("tema")
                descripcion = data.get("descripcion")
                cuestionario_guardar = data.get("cuestionario")
                cuestionario = Cuestionarios(
                    nombre_cuestionario=nombre_cuestionario,
                    id_tema_fk=Temas.objects.get(id=tema),
                    nombre_usuario_fk=Usuarios.objects.get(username=request.user),
                    descripcion_cuestionario=descripcion
                )

                cuestionario.save()

                preguntas = [Preguntas(pregunta=pregunta["pregunta"],id_cuestionario_fk=cuestionario) for pregunta in cuestionario_guardar]

                for pregunta in preguntas:
                    pregunta.save()

                respuestas = []
                for posicion_pregunta in range(len(cuestionario_guardar)):
                    for respuesta in cuestionario_guardar[posicion_pregunta]["opciones"]:
                        # print(f"Respuesta: {respuesta} Correcta: {cuestionario_guardar[posicion_pregunta]["respuesta_correcta"]}")
                        respuestas.append(Respuestas(respuesta=respuesta,
                        correcta=True if cuestionario_guardar[posicion_pregunta]["opciones"][cuestionario_guardar[posicion_pregunta]["respuesta_correcta"]] == respuesta else False,
                        id_pregunta_fk=preguntas[posicion_pregunta]))
                                
                for respuesta in respuestas:
                    respuesta.save()

                return JsonResponse({"success": True,"idCuestionario":cuestionario.id})

        except Exception as error:
            print("Error: ",error)
    

class ContestarCuestionarioView(View):


    def get(self,request,cuestionario_id):
        cuestionario = Cuestionarios.objects.get(id=cuestionario_id)
        preguntas = Preguntas.objects.filter(id_cuestionario_fk=cuestionario)
        respuestas = Respuestas.objects.filter(id_pregunta_fk__in=preguntas)
        preguntas_respuestas = [
            {
                "pregunta": pregunta,
                "respuestas": [respuesta for respuesta in respuestas if respuesta.id_pregunta_fk == pregunta]
            }
            for pregunta in preguntas
        ]
        return render(request, "cuestionarios/contestar.html", {"cuestionario": cuestionario, "preguntas": preguntas_respuestas,})

    def post(self,request,cuestionario_id):

        preguntas = Preguntas.objects.filter(id_cuestionario_fk=cuestionario_id)
        respuestas_usuario_correctas_falladas = []
        respuestas = Respuestas.objects.filter(id_pregunta_fk__in=preguntas)
        preguntas_respuestas = [
            {
                "pregunta": pregunta,
                "respuestas": [respuesta for respuesta in respuestas if respuesta.id_pregunta_fk == pregunta]
            }
            for pregunta in preguntas
        ]
        aciertos = 0
        falladas = 0
        aprobado = False
        for id_pregunta in request.POST:
            if id_pregunta.isdigit():
                respuesta_correcta = Respuestas.objects.get(id_pregunta_fk=id_pregunta,correcta=True)
                respuesta_usuario = request.POST[id_pregunta]
                respuesta_usuario_objeto = Respuestas.objects.get(id=respuesta_usuario,id_pregunta_fk=id_pregunta)
                cuestionario = Cuestionarios.objects.get(id=cuestionario_id)
                acierto = False
                if int(respuesta_usuario) == respuesta_correcta.id:
                    print(f"Usuario acerto en la pregunta {id_pregunta} y en la respuesta {respuesta_correcta.respuesta}")
                    acierto = True
                    aciertos += 1
                else:
                    print(f"Usuario fallo en la pregunta {id_pregunta} y en la respuesta {respuesta_usuario}")
                    acierto = False
                    falladas += 1
                
                for pregunta in preguntas_respuestas:
                    if int(id_pregunta) == pregunta["pregunta"].id:
                        pregunta["acierto"] = acierto
                        pregunta["respuesta_correcta"] = respuesta_correcta
                        pregunta["respuesta_usuario"] = respuesta_usuario_objeto
                        print("respuesta usuario: ",respuesta_usuario_objeto.id)
                        
                print(f"Respuesta correcta es: {respuesta_correcta.respuesta} y el usuario respondio {respuesta_usuario}")
                
                respuestas_usuario_correctas_falladas.append({id_pregunta:{"correcta":respuesta_correcta.id,"usuario":respuesta_usuario}})
        nota_aprobar = len(preguntas_respuestas) / 2
        if aciertos >= nota_aprobar:
            aprobado = True
        print(preguntas_respuestas)
        # nombre_usuario_fk = models.ForeignKey(Usuarios,on_delete=models.CASCADE)
        # id_cuestionario_fk = models.ForeignKey(Cuestionarios,on_delete=models.PROTECT,null=True)
        # id_tema_fk = models.ForeignKey(Temas,on_delete=models.CASCADE)
        # acertadas = models.IntegerField(null=False)
        # falladas = models.IntegerField(null=False)
        # porcentaje_acierto = models.FloatField(null=False)
        porcentaje_acierto = aciertos / len(preguntas_respuestas) * 100
        print("CUESTIONARIO ID: ",cuestionario.id_tema_fk.id)
        print("PORCENTAJE ACIERTO: ",porcentaje_acierto)
        # usuario = Usuarios.objects.get(username=request.user)
        estadistica = Estadisticas(nombre_usuario_fk=request.user,id_cuestionario_fk=cuestionario,id_tema_fk=cuestionario.id_tema_fk,
                                   acertadas=aciertos,falladas=falladas,porcentaje_acierto=porcentaje_acierto)
        estadistica.save()
        return render(request,"cuestionarios/contestado.html",{"respuesta_usuario":respuestas_usuario_correctas_falladas,
                                                             "preguntas":preguntas_respuestas,"cuestionario":cuestionario,
                                                             "aciertos":aciertos,"falladas":falladas,"aprobado":aprobado})