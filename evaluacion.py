import streamlit as st
import time
import random

# ==========================================
# BANCO DE 50 PREGUNTAS (4 RUBROS)
# Opciones ponderadas: [Riesgo (0), Dudoso (5), Seguro/Ético (20)]
# ==========================================
banco_preguntas = {
    "Seguridad y Riesgos Críticos": [
        {"id": "S1", "texto": "Si un neumático presenta un desgaste leve en el límite y cambiarlo retrasa la salida 2 horas, ¿qué haces?", "opciones": ["Salgo a la ruta, un desgaste leve no causará un accidente hoy.", "Aviso al supervisor, pero si me presiona, inicio la ruta.", "Detengo la salida y exijo el cambio de neumático."], "puntajes": [0, 5, 20]},
        {"id": "S2", "texto": "¿Con qué frecuencia omites el check-list pre-uso si llegas tarde?", "opciones": ["Frecuentemente, si conozco el vehículo.", "A veces, solo reviso lo más básico rápido.", "Nunca, el check-list es obligatorio siempre."], "puntajes": [0, 5, 20]},
        {"id": "S3", "texto": "Un pasajero pide que aceleres en una recta despejada para llegar a tiempo. ¿Qué haces?", "opciones": ["Acelero un poco, no hay peligro en la recta.", "Le explico que no puedo, pero intento recuperar tiempo en las curvas.", "Mantengo la velocidad permitida y le explico las normas de seguridad."], "puntajes": [0, 5, 20]},
        {"id": "S4", "texto": "Notas una falla leve en los frenos que desaparece al calentar. ¿Qué haces?", "opciones": ["Sigo la ruta, es normal en frío.", "Lo anoto al final del turno para que lo revisen mañana.", "Reporto de inmediato y pido revisión antes de salir."], "puntajes": [0, 5, 20]},
        {"id": "S5", "texto": "¿Qué haces si te encuentras con neblina muy densa y visibilidad casi nula?", "opciones": ["Sigo conduciendo despacio pegado al vehículo de adelante.", "Enciendo luces intermitentes y sigo a velocidad media.", "Me detengo en un lugar seguro hasta que la visibilidad mejore."], "puntajes": [0, 5, 20]},
        {"id": "S6", "texto": "El cinturón de seguridad del piloto se traba a veces. ¿Qué decides?", "opciones": ["Conduzco así, soy cuidadoso.", "Intento arreglarlo yo mismo con alguna herramienta.", "No opero el vehículo hasta que lo repare mantenimiento."], "puntajes": [0, 5, 20]},
        {"id": "S7", "texto": "Un supervisor te dice que excedas la velocidad un poco porque hay un cliente VIP. ¿Cómo reaccionas?", "opciones": ["Obedezco, es una orden directa.", "Trato de ir al límite exacto, rozando el exceso.", "Me niego respetuosamente argumentando las políticas de seguridad."], "puntajes": [0, 5, 20]},
        {"id": "S8", "texto": "¿Qué opinas de los reportes de incidentes sin daños (casi accidentes)?", "opciones": ["Son pérdida de tiempo.", "Solo los lleno si el supervisor me vio.", "Son vitales para prevenir accidentes futuros."], "puntajes": [0, 5, 20]},
        {"id": "S9", "texto": "Estás a punto de adelantar a un camión lento, pero hay doble línea continua. ¿Qué haces?", "opciones": ["Adelanto rápido si no viene nadie.", "Pito para que se orille y lo paso por la berma.", "Espero con paciencia hasta la zona de adelantamiento permitido."], "puntajes": [0, 5, 20]},
        {"id": "S10", "texto": "¿Cuál es tu prioridad al encender el minibus?", "opciones": ["Poner música y ajustar el aire.", "Verificar los espejos rápidamente.", "Hacer la prueba de frenos, luces y panel de control."], "puntajes": [0, 5, 20]},
        {"id": "S11", "texto": "Si hay un derrame de aceite pequeño en la cabina, ¿cómo actúas?", "opciones": ["Le pongo un cartón encima.", "Lo limpio por encima y sigo.", "Reporto el riesgo de resbalamiento y pido limpieza profunda."], "puntajes": [0, 5, 20]},
        {"id": "S12", "texto": "Un pasajero no quiere ponerse el cinturón de seguridad. ¿Qué haces?", "opciones": ["Arranco igual, es su problema.", "Le pido por favor y si no quiere, arranco.", "Me niego a iniciar la marcha hasta que se lo ponga."], "puntajes": [0, 5, 20]},
        {"id": "S13", "texto": "Llevas carga suelta en el pasillo por falta de espacio. ¿Qué decides?", "opciones": ["Acomodo a los pasajeros alrededor.", "Voy despacio para que no se ruede.", "No permito carga en las vías de evacuación."], "puntajes": [0, 5, 20]}
    ],
    "Gestión de la Fatiga y Somnolencia": [
        {"id": "F1", "texto": "Dormiste solo 3 horas por un tema personal. Llegas a tu turno, ¿qué haces?", "opciones": ["Tomo bebidas energizantes y salgo.", "Le digo al supervisor que me ponga en una ruta corta.", "Reporto fatiga e inaptitud para conducir."], "puntajes": [0, 5, 20]},
        {"id": "F2", "texto": "Sientes pesadez en los ojos a 20 minutos de llegar. ¿Qué haces?", "opciones": ["Abro la ventana, pongo música fuerte y llego.", "Me mojo la cara en marcha.", "Detengo el vehículo, aplico pausas activas y aviso a base."], "puntajes": [0, 5, 20]},
        {"id": "F3", "texto": "¿Qué opinas del uso de energizantes para combatir el sueño en la ruta?", "opciones": ["Son la mejor herramienta del conductor.", "Los uso solo cuando ya no aguanto más.", "Son un riesgo; ocultan el agotamiento real."], "puntajes": [0, 5, 20]},
        {"id": "F4", "texto": "Tu relevo no llega y te piden conducir 4 horas más excediendo tu límite. ¿Qué haces?", "opciones": ["Acepto, quiero las horas extras.", "Acepto si me dan café.", "Me niego por exceder la jornada máxima segura."], "puntajes": [0, 5, 20]},
        {"id": "F5", "texto": "Bostezas repetidamente en la ruta. ¿Qué significa para ti?", "opciones": ["Nada, es aburrimiento.", "Falta de aire, abro la ventana.", "Alerta temprana de fatiga; debo detenerme."], "puntajes": [0, 5, 20]},
        {"id": "F6", "texto": "Si tienes un microsueño (cabeceo) de un segundo, ¿cómo reaccionas?", "opciones": ["Me asusto y sigo manejando más alerta.", "Tomo agua.", "Es una alerta crítica; me detengo de inmediato."], "puntajes": [0, 5, 20]},
        {"id": "F7", "texto": "¿Cuántas horas de sueño consideras necesarias para un turno de 8 horas?", "opciones": ["Con 4 o 5 horas estoy bien.", "Depende del día.", "Mínimo 7 a 8 horas ininterrumpidas."], "puntajes": [0, 5, 20]},
        {"id": "F8", "texto": "En tus días de descanso, ¿tienes otro trabajo manejando?", "opciones": ["Sí, taxeo para ganar más.", "A veces hago fletes cortos.", "No, respeto mi descanso para recuperarme."], "puntajes": [0, 5, 20]},
        {"id": "F9", "texto": "¿Qué comes antes de un viaje largo nocturno?", "opciones": ["Comida pesada para no tener hambre.", "Lo que haya disponible.", "Comida ligera e hidratación constante."], "puntajes": [0, 5, 20]},
        {"id": "F10", "texto": "Sientes calambres y dolor de espalda a mitad de camino. ¿Qué haces?", "opciones": ["Aguanto el dolor hasta llegar.", "Me acomodo en el asiento mientras manejo.", "Me detengo y hago estiramientos musculares."], "puntajes": [0, 5, 20]},
        {"id": "F11", "texto": "¿Crees que la experiencia te hace inmune al sueño al volante?", "opciones": ["Totalmente, el cuerpo se acostumbra.", "Un poco, ayuda a controlarlo.", "Totalmente en desacuerdo, la fatiga es biológica."], "puntajes": [0, 5, 20]},
        {"id": "F12", "texto": "Tu compañero de doble cabina se queda dormido en su turno. ¿Qué haces?", "opciones": ["Lo dejo dormir y yo sigo manejando.", "Lo despierto gritando.", "Tomo el control en lugar seguro y reporto el incidente."], "puntajes": [0, 5, 20]},
        {"id": "F13", "texto": "Tomas un medicamento para la gripe que da somnolencia. ¿Qué haces?", "opciones": ["Lo tomo y manejo con cuidado.", "Me tomo la mitad de la dosis.", "Reporto al área médica y no conduzco."], "puntajes": [0, 5, 20]}
    ],
    "Integridad y Cumplimiento Ético": [
        {"id": "I1", "texto": "¿Qué haces si ves que otros conductores venden combustible del vehículo?", "opciones": ["Nada, no me meto en problemas de otros.", "Les digo que tengan cuidado.", "Lo reporto de manera confidencial a la empresa."], "puntajes": [0, 5, 20]},
        {"id": "I2", "texto": "Raspan la pintura del minibus retrocediendo y nadie vio. ¿Qué haces?", "opciones": ["No digo nada.", "Lo limpio para que pase desapercibido.", "Lo reporto en mi hoja de inspección."], "puntajes": [0, 5, 20]},
        {"id": "I3", "texto": "Un compañero te pide que registres su llegada antes de tiempo. ¿Qué haces?", "opciones": ["Lo hago, es un favor de amigos.", "Le digo que lo haga otro.", "Me niego, es una falsificación de registros."], "puntajes": [0, 5, 20]},
        {"id": "I4", "texto": "¿Desviar el minibus unas cuadras para un asunto personal está bien?", "opciones": ["Sí, si no me tardo.", "Solo si no llevo pasajeros.", "No, el uso del vehículo es estrictamente laboral."], "puntajes": [0, 5, 20]},
        {"id": "I5", "texto": "Encuentras una billetera perdida en el minibus. ¿Qué haces?", "opciones": ["Me quedo con el efectivo y boto lo demás.", "La dejo ahí por si el dueño vuelve.", "La entrego de inmediato a objetos perdidos/seguridad."], "puntajes": [0, 5, 20]},
        {"id": "I6", "texto": "Has tomado una cerveza 4 horas antes de tu turno. ¿Qué decides?", "opciones": ["Voy a trabajar, ya se me pasó.", "Mastico chicle y uso perfume.", "Llamo avisando que no estoy en condiciones de operar."], "puntajes": [0, 5, 20]},
        {"id": "I7", "texto": "Un cliente te ofrece dinero para llevar un paquete no registrado. ¿Qué haces?", "opciones": ["Acepto, un dinero extra no cae mal.", "Reviso qué es y si es seguro, lo llevo.", "Lo rechazo tajantemente, rompe la política de la empresa."], "puntajes": [0, 5, 20]},
        {"id": "I8", "texto": "El sensor GPS del vehículo está fallando. ¿Qué pasa por tu mente?", "opciones": ["Qué bueno, así no me controlan hoy.", "No le doy importancia.", "Lo reporto urgente para que lo recalibren."], "puntajes": [0, 5, 20]},
        {"id": "I9", "texto": "Sanción ideal para quien altera una prueba de alcoholemia:", "opciones": ["Llamado de atención verbal.", "Suspensión de unos días.", "Despido inmediato."], "puntajes": [0, 5, 20]},
        {"id": "I10", "texto": "Si llegas tarde por quedarte dormido, ¿qué excusa das?", "opciones": ["Invento que hubo tráfico pesado.", "Digo que el minibus no encendía.", "Digo la verdad y asumo la responsabilidad."], "puntajes": [0, 5, 20]},
        {"id": "I11", "texto": "Faltan herramientas en el kit de emergencia. ¿Qué haces?", "opciones": ["Me robo unas de otro vehículo.", "No digo nada para que no me culpen.", "Reporto el faltante para reposición."], "puntajes": [0, 5, 20]},
        {"id": "I12", "texto": "¿Mentirías en un reporte de accidente para salvar el trabajo de un amigo?", "opciones": ["Sí, la lealtad es primero.", "Solo ocultaría detalles menores.", "No, la integridad del reporte es innegociable."], "puntajes": [0, 5, 20]}
    ],
    "Estabilidad Emocional y Trabajo Bajo Presión": [
        {"id": "E1", "texto": "Un auto se cruza bruscamente obligándote a frenar fuerte. ¿Tu reacción?", "opciones": ["Lo persigo para insultarlo.", "Toco el claxon repetidamente y me enojo.", "Respiro, retomo la calma y sigo la ruta."], "puntajes": [0, 5, 20]},
        {"id": "E2", "texto": "Tráfico detenido, pasajeros te insultan por el retraso. ¿Qué haces?", "opciones": ["Les grito que no es mi culpa.", "Me pongo audífonos y los ignoro.", "Les explico la situación con calma y empatía."], "puntajes": [0, 5, 20]},
        {"id": "E3", "texto": "Tu supervisor te regaña injustamente frente a todos. ¿Qué haces?", "opciones": ["Le respondo a gritos ahí mismo.", "Me voy del lugar dejando tirado el trabajo.", "Mantengo la calma y pido hablar en privado después."], "puntajes": [0, 5, 20]},
        {"id": "E4", "texto": "El minibus se avería en zona sin señal y con frío. ¿Primer paso?", "opciones": ["Entro en pánico y dejo que los pasajeros resuelvan.", "Me enojo y pateo la llanta.", "Aseguro el vehículo, calmo a los pasajeros y busco cómo comunicar."], "puntajes": [0, 5, 20]},
        {"id": "E5", "texto": "Llevas 3 horas de retraso por factores externos. ¿Cómo te sientes?", "opciones": ["Desesperado y conduzco agresivamente.", "Estresado pero intentando apurarme.", "Enfocado en llegar seguro, el tiempo ya se perdió."], "puntajes": [0, 5, 20]},
        {"id": "E6", "texto": "Un pasajero ebrio empieza a molestar a otros. ¿Qué haces?", "opciones": ["Me meto a pelear físicamente con él.", "No hago nada mientras no me moleste a mí.", "Detengo el vehículo y coordino apoyo de seguridad."], "puntajes": [0, 5, 20]},
        {"id": "E7", "texto": "¿Cómo reaccionas cuando un conductor lento no te deja pasar?", "opciones": ["Me pego mucho a su parachoque (tailgating).", "Le hago luces todo el tiempo.", "Mantengo distancia segura hasta que pueda adelantar."], "puntajes": [0, 5, 20]},
        {"id": "E8", "texto": "Si recibes una mala noticia familiar antes de conducir, ¿qué haces?", "opciones": ["Conduzco llorando o alterado.", "Trato de no pensar en ello.", "Informo que no estoy emocionalmente apto para conducir hoy."], "puntajes": [0, 5, 20]},
        {"id": "E9", "texto": "Te equivocas de ruta y te pierdes. Los pasajeros se quejan. ¿Qué haces?", "opciones": ["Me molesto y les digo que se callen.", "Sigo manejando a ciegas a ver si encuentro el camino.", "Me detengo, pido disculpas y uso el mapa/radio para ubicarme."], "puntajes": [0, 5, 20]},
        {"id": "E10", "texto": "¿Qué tan frecuente te enojas al volante?", "opciones": ["Todos los días, el tráfico es insoportable.", "A veces, cuando cometen imprudencias.", "Casi nunca, trato de ser tolerante y defensivo."], "puntajes": [0, 5, 20]},
        {"id": "E11", "texto": "El cobrador o copiloto comete un error grave. ¿Cómo se lo dices?", "opciones": ["Lo insulto delante de los pasajeros.", "Le digo que no sirve para el trabajo.", "Le hago la corrección en privado y con respeto."], "puntajes": [0, 5, 20]},
        {"id": "E12", "texto": "Las reglas de la empresa cambian repentinamente. ¿Tu actitud?", "opciones": ["Me quejo y me resisto a cumplirlas.", "Las cumplo de mala gana.", "Me adapto rápidamente por el bien de la operación."], "puntajes": [0, 5, 20]}
    ]
}

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Evaluación Midot - Conductores", layout="centered", page_icon="🚐")

st.title("🚐 Evaluación de Integridad y Riesgos Críticos")
st.markdown("Esta prueba consta de **30 preguntas** seleccionadas para evaluar toma de decisiones, control de fatiga e integridad operativa.")

# ==========================================
# LÓGICA DE SELECCIÓN ALEATORIA DE PREGUNTAS
# ==========================================
# Para elegir 30 preguntas, seleccionamos 8, 8, 7, y 7 de los rubros
if 'preguntas_seleccionadas' not in st.session_state:
    st.session_state.start_time = time.time()
    
    seleccion = []
    # Seleccionamos una cantidad fija por categoría para equilibrar
    seleccion.extend(random.sample(banco_preguntas["Seguridad y Riesgos Críticos"], 8))
    seleccion.extend(random.sample(banco_preguntas["Gestión de la Fatiga y Somnolencia"], 8))
    seleccion.extend(random.sample(banco_preguntas["Integridad y Cumplimiento Ético"], 7))
    seleccion.extend(random.sample(banco_preguntas["Estabilidad Emocional y Trabajo Bajo Presión"], 7))
    
    # Mezclamos el orden final para que no aparezcan por bloque
    random.shuffle(seleccion)
    st.session_state.preguntas_seleccionadas = seleccion

# ==========================================
# INTERFAZ DEL FORMULARIO
# ==========================================
with st.form("eval_form"):
    st.info("Responde con la mayor honestidad posible. Todas las preguntas son obligatorias.")
    
    for i, p in enumerate(st.session_state.preguntas_seleccionadas):
        st.markdown(f"**{i+1}. {p['texto']}**")
        # Generar las opciones
        st.radio(
            label="Selecciona una opción:",
            options=p['opciones'],
            key=p['id'], # Usamos el ID como llave única en session_state
            label_visibility="collapsed"
        )
        st.divider()

    submit = st.form_submit_button("Finalizar Evaluación")

# ==========================================
# CÁLCULO DE RESULTADOS AL ENVIAR
# ==========================================
if submit:
    puntaje_total = 0
    puntaje_maximo = 30 * 20 # 30 preguntas x 20 puntos máximo cada una = 600 puntos

    for p in st.session_state.preguntas_seleccionadas:
        respuesta_usuario = st.session_state[p['id']]
        indice_respuesta = p['opciones'].index(respuesta_usuario)
        puntaje_obtenido = p['puntajes'][indice_respuesta]
        puntaje_total += puntaje_obtenido

    porcentaje_final = round((puntaje_total / puntaje_maximo) * 100, 2)
    tiempo_total = round(time.time() - st.session_state.start_time, 2)
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)

    # Mostrar Resultados
    st.header("📊 Resultados del Perfil")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Índice de Confiabilidad Operativa", f"{porcentaje_final}%")
    with col2:
        st.metric("Tiempo de Completado", f"{minutos} min {segundos} seg")
        
    # Interpretación Estilo MIDOT
    if porcentaje_final >= 85:
        st.success("✅ **PERFIL RECOMENDADO:** El candidato posee una sólida cultura preventiva, respeto por las normas e integridad ética.")
    elif porcentaje_final >= 65:
        st.warning("⚠️ **PERFIL EN OBSERVACIÓN:** Perfil con áreas de mejora. Puede ceder bajo presión sacrificando la seguridad operativa. Requiere supervisión.")
    else:
        st.error("❌ **ALTO RIESGO OPERATIVO:** Respuestas incompatibles con la seguridad vial y el código de ética. Alta probabilidad de negligencia o conductas contraproducentes.")

    # Opción para reiniciar el test corregida
    if st.button("Realizar nueva evaluación"):
        # Limpiamos el estado para generar nuevas preguntas
        del st.session_state.preguntas_seleccionadas
        st.rerun()
