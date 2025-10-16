from datetime import datetime
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views import View
from cuestionarios.models import Cuestionarios, Estadisticas, Preguntas, Respuestas,Temas
from django.db.models import Avg,Sum
from django.db.models.functions import TruncMonth,TruncYear,TruncDate
from calendar import month_name

class EstadisticasView(View):

    def get(self, request):

        return render(request, 'estadisticas/estadisticas.html')

class EstadisticasGeneralesView(View):

    def get(self,request,tipo):

        estadisticas_json = {}
        estadisticas_generales = Estadisticas.objects.all()        
        temas = Temas.objects.all()
        if tipo == "general":
            for tema in temas:
                #Consulta para obtener todos los cuestionarios respondidos
                # de un tema especifico del usuarios
                estadisticas_cuestionarios_tema = estadisticas_generales.filter(
                    id_tema_fk = tema.id,
                    nombre_usuario_fk=request.user
                )

                total_preguntas_respondidas = 0
                total_respuestas_acertadas = 0
                cuestionarios_tema_ids = estadisticas_cuestionarios_tema.values_list("id_cuestionario_fk",flat=True)
                conteo_preguntas_cuestionario = Preguntas.objects.filter(
                    id_cuestionario_fk__in=cuestionarios_tema_ids
                )
                preguntas_ids = conteo_preguntas_cuestionario.values_list("id",flat=True)
                conteo_respuestas_aciertos = Respuestas.objects.filter(
                    id_pregunta_fk__in=preguntas_ids,
                    correcta=True
                ).count()
                total_preguntas_respondidas = conteo_preguntas_cuestionario.count()
                print(f"PRUEBA VALUES_LIST: {total_preguntas_respondidas}")

                estadisticas_json[tema.nombre] = {
                    "cuestionarios_acertados":estadisticas_generales.filter(
                        porcentaje_acierto__gte = 50.0,id_tema_fk = tema.id,
                        nombre_usuario_fk=request.user
                    ).count(),
                    "cuestionarios_suspendidos":estadisticas_generales.filter(
                        porcentaje_acierto__lt = 50.0,id_tema_fk = tema.id,
                        nombre_usuario_fk=request.user
                    ).count(),
                    "cuestionarios_realizados":estadisticas_generales.filter(
                        id_tema_fk = tema.id,
                        nombre_usuario_fk=request.user
                    ).count(),
                    "preguntas_respondidas":total_preguntas_respondidas,
                    "respuestas_acertadas":conteo_respuestas_aciertos,
                    "nota_promedio":round(estadisticas_generales.filter(
                        id_tema_fk = tema.id,
                        nombre_usuario_fk=request.user
                    ).aggregate(
                        promedio=Avg('porcentaje_acierto') / 10
                    )['promedio'] or 0.0,2)
                }
                
            return JsonResponse(estadisticas_json)
        elif tipo == "historico":
            desde = request.GET.get("desde","")
            hasta = request.GET.get("hasta","")
            por_anio = request.GET.get("anio","")
            por_mes = request.GET.get("mes","")
            print("Desde: ",desde)
            print("Hasta: ",hasta)
            if por_mes == "1" and por_anio == "":
                estadisticas_por_mes = (
                    Estadisticas.objects.filter(
                        nombre_usuario_fk=request.user
                    ).values('fecha_creacion')
                    .annotate(
                        mes=TruncMonth('fecha_creacion')
                    ).values("mes")
                    .annotate(conteo_aciertos=Sum('acertadas'))
                    .order_by('mes')[:12]
                )

                for estadistica in estadisticas_por_mes:
                    mes = f"{month_name[estadistica["mes"].month]}-{estadistica["mes"].year}"
                    estadisticas_json[mes] = estadistica['conteo_aciertos']
                    print(mes)
            elif por_mes == "" and por_anio == "1":
                estadisticas_por_anio = (
                    Estadisticas.objects.filter(
                        nombre_usuario_fk=request.user
                    ).values('fecha_creacion')
                    .annotate(
                        anio=TruncYear('fecha_creacion')
                    ).values("anio")
                    .annotate(conteo_aciertos=Sum('acertadas'))
                    .order_by('anio')
                    
                )
                for estadistica in estadisticas_por_anio:
                    estadisticas_json[f'{estadistica["anio"].year}'] = estadistica['conteo_aciertos']

            elif desde != "" and hasta != "":
                desde = datetime.strptime(desde, "%Y-%m-%d")
                desde = desde.replace(hour=23, minute=59, second=59)
                hasta = datetime.strptime(hasta, "%Y-%m-%d")
                hasta = hasta.replace(hour=23, minute=59, second=59)
                print("DESDE: ",desde)
                print("HASTA: ",hasta)
                estadisticas_por_fecha = (
                    Estadisticas.objects.filter(
                        nombre_usuario_fk=request.user,
                        fecha_creacion__gte=desde,
                        fecha_creacion__lte=hasta
                    ).values('fecha_creacion')
                    .annotate(
                        fecha=TruncDate('fecha_creacion')
                    ).values("fecha")
                    .annotate(conteo_aciertos=Sum('acertadas'))
                    .order_by('fecha')
                )
                for estadistica in estadisticas_por_fecha:
                    estadisticas_json[f'{estadistica["fecha"]}'] = estadistica['conteo_aciertos']
            
            return JsonResponse(estadisticas_json)
        
        else:
            return redirect('estadisticas')