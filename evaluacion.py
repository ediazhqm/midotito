import streamlit as st
import time
import random

# ==============================================================================
# BANCO DE 50 PREGUNTAS PROFUNDAS (ENFOQUE SITUATIONAL JUDGMENT TEST - SJT)
# Diseñado para mitigar la deseabilidad social y evaluar comportamiento real.
# Ponderación oculta por opción: [Riesgo/Normalización (0), Pragmático/Dudoso (10), Control Crítico (20)]
# ==============================================================================
banco_preguntas = {
    "Seguridad y Riesgos Críticos": [
        {
            "id": "S1",
            "texto": "La operación tiene 45 minutos de retraso y los pasajeros exigen salir. El check-list pre-uso detallado toma 15 minutos. ¿Cuál es la práctica más realista en el rubro?",
            "opciones": [
                "Iniciar la marcha para calmar a los pasajeros y hacer el check-list en la primera parada.",
                "Hacer una revisión visual rápida (3 min) enfocada solo en frenos y llantas para mitigar la molestia.",
                "Ejecutar el check-list de 15 minutos completos, asumiendo las quejas formales de los pasajeros."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S2",
            "texto": "Basado en tu experiencia en el sector, ¿qué porcentaje de pilotos crees que, bajo mucha presión, ha omitido reportar un casi-accidente (incidente sin daños) para evitar papeleo?",
            "opciones": [
                "Más del 60%, es una práctica común para no detener la operación.",
                "Alrededor del 30%, solo cuando consideran que el evento no fue realmente grave.",
                "Menos del 10%, la mayoría entiende que reportar incidentes menores previene fatalidades futuras."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S3",
            "texto": "Un procedimiento estricto exige detener el vehículo si falla el sensor de retroceso, pero tú tienes 15 años de experiencia estacionando sin sensores. ¿Qué consideras más adecuado?",
            "opciones": [
                "Continuar operando con precaución extrema; la experiencia acumulada suple al sensor temporalmente.",
                "Pedir a un compañero que actúe de vigía improvisado cada vez que retroceda hasta terminar el turno.",
                "Detener el equipo inmediatamente. Operar sin un control de riesgo crítico activo es inaceptable."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S4",
            "texto": "¿Qué opinas de la siguiente afirmación: 'A veces, los supervisores de HSEQ diseñan reglas desde un escritorio que en la ruta real son imposibles de cumplir al 100%'?",
            "opciones": [
                "Totalmente de acuerdo, la teoría a menudo choca con la realidad y las metas operativas diarias.",
                "Parcialmente de acuerdo, algunas reglas son ambiguas y requieren adaptación flexible en campo.",
                "En desacuerdo, si una regla parece imposible, indica un fallo de planificación, no una excusa para omitirla."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S5",
            "texto": "Durante una ruta nocturna, un pasajero VIP te exige que superes el límite de velocidad en 10 km/h o presentará una queja que afectará tu bono de desempeño. ¿Qué haces?",
            "opciones": [
                "Acelero levemente solo en tramos rectos donde mi destreza técnica garantiza el control total.",
                "Le explico que los límites están monitoreados por telemetría/GPS para excusarme y evitar el conflicto.",
                "Mantengo la velocidad de norma de forma inflexible y le ofrezco el libro de reclamaciones si no está conforme."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S6",
            "texto": "El cinturón de seguridad del piloto se traba de forma intermitente, pero aplicando cierta fuerza y maña se logra enganchar. ¿Qué decides?",
            "opciones": [
                "Conduzco aplicando la maña para engancharlo; lo importante es estar sujeto y no retrasar el viaje.",
                "Conduzco sin engancharlo en los tramos cortos internos donde el riesgo de colisión es mínimo.",
                "No opero la unidad hasta que el área de mantenimiento reemplace el mecanismo por completo."
            ],
            "puntajes": [10, 0, 20]
        },
        {
            "id": "S7",
            "texto": "En el gremio de transportistas, si una regla de seguridad corporativa ralentiza el flujo del cliente, ¿qué se suele hacer de forma habitual?",
            "opciones": [
                "Omitirla discretamente si se sabe que en ese tramo no hay fiscalización ni cámaras de video.",
                "Adaptar el procedimiento a medias para intentar cumplir tanto con el cliente como con la norma.",
                "Cumplirla estrictamente al 100%, asumiendo el impacto en los tiempos y la molestia del cliente."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S8",
            "texto": "Una alarma menor del tablero parpadea de forma intermitente, pero el motor se escucha perfecto y los niveles están bien. ¿Cómo procedes?",
            "opciones": [
                "Ignoro la luz hasta el final del día para no generar pánico ni retrasar las salidas programadas.",
                "Apago y enciendo el motor para resetear el sistema eléctrico esperando que la alerta desaparezca.",
                "Reporto de inmediato a la base y espero la autorización del mecánico técnico antes de avanzar un metro."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S9",
            "texto": "Estás detrás de un vehículo pesado que avanza a 10 km/h en una zona con doble línea continua, pero tienes visibilidad perfecta y no viene nadie. ¿Qué haces?",
            "opciones": [
                "Adelanto rápido de forma segura; la línea continua está desactualizada para este tipo de escenarios.",
                "Le hago luces o toco la bocina para que se desvíe a la berma y me deje pasar sin pisar la línea.",
                "Me mantengo detrás a la misma velocidad hasta encontrar una zona de adelantamiento legalmente permitida."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S10",
            "texto": "Un bache profundo ha aparecido en tu ruta habitual. No está señalizado por la autoridad. ¿Cómo gestionas este obstáculo?",
            "opciones": [
                "Lo esquivo realizando una maniobra rápida invadiendo ligeramente el carril contrario si se ve despejado.",
                "Freno bruscamente justo antes de impactarlo para minimizar el daño mecánico a la suspensión.",
                "Reduzco la velocidad con mucha anticipación obligando a los vehículos de atrás a frenar de forma segura."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S11",
            "texto": "La presión de un neumático trasero marca 5 PSI menos de lo estipulado. Inflarla requiere desviarse 20 minutos de la ruta programada. ¿Qué acción tomas?",
            "opciones": [
                "Continuar la ruta prestando atención visual en cada parada técnica; 5 PSI no desestabilizan el bus.",
                "Completar el tramo de ida con los pasajeros y corregir la presión en el taller central al retornar.",
                "Desviarme de inmediato a la estación de servicio; la baja presión altera la adherencia crítica en curvas."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S12",
            "texto": "Sinceramente, ¿cuál crees que es la verdadera utilidad de las auditorías de seguridad sorpresa en ruta?",
            "opciones": [
                "Son una medida burocrática e inquisitiva que interrumpe innecesariamente el ritmo de trabajo habitual.",
                "Son útiles principalmente para supervisar a los pilotos nuevos o aquellos con antecedentes de incidentes.",
                "Son herramientas esenciales que obligan a mantener los estándares preventivos activos en todo momento."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "S13",
            "texto": "Tienes un paquete de herramientas pequeño suelto sobre el tablero del minibus. ¿Dónde debería estar según tu criterio técnico?",
            "opciones": [
                "Puede quedarse ahí si no obstruye de forma directa la visibilidad del parabrisas delantero.",
                "Se puede asegurar firmemente con una banda elástica o cinta adhesiva sobre el mismo tablero.",
                "Debe guardarse obligatoriamente en la guantera o en un compartimento cerrado diseñado para carga."
            ],
            "puntajes": [0, 10, 20]
        }
    ],
    "Gestión de la Fatiga y Somnolencia": [
        {
            "id": "F1",
            "texto": "Muchos conductores con amplia experiencia afirman que el cuerpo se adapta a dormir solo 4 horas y los reflejos se mantienen intactos. ¿Qué opinas?",
            "opciones": [
                "Es una realidad; el hábito y los años al volante generan una resistencia biológica especial.",
                "Depende de variables individuales como el estado físico, la alimentación y la edad del piloto.",
                "Es un mito sumamente peligroso; la fatiga cognitiva reduce la velocidad de reacción de forma científica."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F2",
            "texto": "En un viaje interprovincial de larga distancia, ¿qué técnica estimas que es la que MÁS aplican los conductores para contener el sueño?",
            "opciones": [
                "Ingerir bebidas energizantes de alta concentración y elevar considerablemente el volumen de la radio.",
                "Bajar por completo las ventanas delanteras para que el aire frío impacte el rostro de forma directa.",
                "Estacionar la unidad en un lugar seguro, reportar la fatiga a la base y dormir una siesta de 20 minutos."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F3",
            "texto": "Atraviesas un problema familiar severo que te ha provocado un alto nivel de estrés y apenas pudiste conciliar el sueño anoche. ¿Cómo evalúas tu capacidad de manejo hoy?",
            "opciones": [
                "Apta; concentrarme en la conducción defensiva me ayudará a despejar la mente de los problemas personales.",
                "Apta bajo automonitoreo; consumiendo café cargado durante el trayecto se compensa la falta de descanso.",
                "No apta; el estrés agudo sumado a la privación de sueño constituye una inaptitud psicofísica inmediata."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F4",
            "texto": "El piloto asignado como tu relevo bosteza de forma reiterada, pero te asegura firmemente que está en óptimas condiciones para conducir. ¿Cómo actúas?",
            "opciones": [
                "Le doy conversación constante durante el viaje para ayudarlo a mantenerse despejado en su turno.",
                "Confío en su palabra profesional; cada conductor experimentado conoce con precisión sus límites reales.",
                "Asumo el volante o exijo detener la unidad; el bostezo repetitivo es un síntoma clínico innegociable."
            ],
            "puntajes": [10, 0, 20]
        },
        {
            "id": "F5",
            "texto": "Si las regulaciones de la empresa eliminaran los topes de horas extra, ¿cuántas horas seguidas crees que un piloto calificado puede manejar con seguridad?",
            "opciones": [
                "Hasta 14 horas continuas, siempre que la compensación económica justifique el esfuerzo extra.",
                "Entre 10 y 12 horas, asumiendo paradas breves para estirar las piernas e hidratarse adecuadamente.",
                "Bajo ninguna circunstancia se deben exceder las horas legales de conducción; el riesgo es exponencial."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F6",
            "texto": "Sientes una pesadez severa en los párpados cuando te encuentras a escasamente 10 minutos de llegar a la estación final. ¿Qué decisión es la más responsable?",
            "opciones": [
                "Incrementar ligeramente la velocidad para finalizar el recorrido antes de sufrir un pestañeo.",
                "Direccionar las rejillas del aire acondicionado frío directo hacia mis ojos para forzar la alerta.",
                "Detener el minibus en la primera zona segura del camino, encender luces y avisar del retraso por fatiga."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F7",
            "texto": "Con total honestidad, ¿qué proporción de pilotos estimas que ha operado con síntomas de somnolencia al menos una vez en el último mes?",
            "opciones": [
                "Más del 70%, las exigencias del mercado y los turnos rotativos hacen que sea casi inevitable.",
                "Alrededor del 40%, sobre todo en las madrugadas o en los tramos más monótonos de la carretera.",
                "Menos del 10%, la gran mayoría respeta rigurosamente sus horas de sueño antes de tomar un servicio."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F8",
            "texto": "Durante tus días oficiales de descanso en un régimen laboral operativo, ¿qué actividad consideras compatible con la seguridad?",
            "opciones": [
                "Realizar servicios de taxi o transporte particular de forma independiente para potenciar la economía familiar.",
                "Ejecutar remodelaciones pesadas o trabajos de construcción pendientes en mi domicilio particular.",
                "Dedicar las jornadas exclusivamente al descanso pasivo, la recreación familiar y la higiene del sueño."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F9",
            "texto": "¿Cómo seleccionas tu alimentación previo a iniciar un servicio de conducción nocturno?",
            "opciones": [
                "Consumo un plato abundante y calórico para evitar la debilidad física y el hambre en la madrugada.",
                "Ingiero cualquier opción disponible en el comedor o ruta sin fijarme en la composición alimenticia.",
                "Opto por una dieta ligera, baja en grasas y carbohidratos simples, priorizando una hidratación constante."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F10",
            "texto": "Si experimentas bostezos frecuentes durante la primera hora de una ruta monótona, ¿cuál suele ser la causa raíz?",
            "opciones": [
                "Un aburrimiento natural provocado por la falta de estímulos visuales en una carretera lineal.",
                "Falta de una adecuada circulación y renovación de oxígeno en el habitáculo interno de la cabina.",
                "Una señal inequívoca de fatiga acumulada o privación de sueño profundo en las noches anteriores."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F11",
            "texto": "¿Qué valoración técnica le otorgas a la implementación de pausas activas obligatorias cada dos horas de conducción?",
            "opciones": [
                "Son una pérdida de tiempo innecesaria que enfría los reflejos y distiende la concentración del piloto.",
                "Son de utilidad moderada, pero solo deberían exigirse si el conductor manifiesta cansancio de forma explícita.",
                "Son controles críticos de ingeniería humana indispensables para prevenir la hipnosis vial y el agarrotamiento."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F12",
            "texto": "Te despiertas para iniciar tu turno con una cefalea intensa y congestión gripal severa. ¿Cómo resuelves la situación?",
            "opciones": [
                "Tomo un antigripal fuerte de venta libre y acudo a operar controlando el malestar de forma personal.",
                "Me presento a laborar normalmente y solicito un relevo médico a la mitad del turno si veo que empeoro.",
                "Reporto la condición al médico ocupacional de retén antes de ingerir cualquier fármaco que induzca somnolencia."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "F13",
            "texto": "Durante un viaje nocturno con clima gélido en el exterior, la calefacción de la cabina genera un ambiente muy confortable. ¿Cómo lo manejas?",
            "opciones": [
                "Mantengo la temperatura alta constante para evitar contracturas musculares por frío.",
                "Subo el brillo de las pantallas del tablero y configuro la radio con música rítmica para balancear.",
                "Regulo la calefacción al mínimo funcional y abro periódicamente deflectores para que ingrese aire fresco."
            ],
            "puntajes": [0, 10, 20]
        }
    ],
    "Integridad y Cumplimiento Ético": [
        {
            "id": "I1",
            "texto": "A nivel general en el transporte, ¿qué porcentaje de conductores crees que usaría el minibus para un desvío personal breve si supiera con certeza que el GPS está inactivo?",
            "opciones": [
                "La gran mayoría (más del 80%), es visto como un beneficio informal tolerable.",
                "Aproximadamente la mitad (50%), dependiendo exclusivamente de la urgencia del asunto personal.",
                "Muy pocos (menos del 10%), la mayoría respeta con rectitud los activos de la organización."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I2",
            "texto": "Un colega muy estimado raya accidentalmente el parachoque del bus. Te pide complicidad para pulirlo él mismo el fin de semana. Si lo reportas, perderá su bono mensual. ¿Qué haces?",
            "opciones": [
                "No comento nada; proteger el bienestar económico de un buen compañero consolida la lealtad de equipo.",
                "Le concedo un plazo de 24 horas para que él mismo efectúe el reporte formal antes de tener que intervenir yo.",
                "Efectúo el reporte de daños de forma inmediata en mi checklist; la transparencia corporativa no es negociable."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I3",
            "texto": "A causa de tus excelentes hábitos de conducción defensiva, tu unidad registra un excedente técnico de combustible al final de la semana. ¿A quién le corresponde ese recurso?",
            "opciones": [
                "Al conductor, como un incentivo o bonificación informal justa por su alta eficiencia operativa.",
                "Se debe almacenar en galoneras externas para resolver contingencias o emergencias del equipo en la ruta.",
                "Es propiedad estricta de la compañía y debe permanecer registrado en los tanques para la siguiente jornada."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I4",
            "texto": "¿Bajo qué circunstancias consideras justificable modificar sutilmente un registro manual de horas de llegada para salvar al equipo de una penalización injusta?",
            "opciones": [
                "Totalmente justificable, el rol principal de un equipo sólido es defenderse de la burocracia excesiva.",
                "Es un recurso comprensible en situaciones extremas, aunque se debe procurar evitar que se vuelva rutina.",
                "Es completamente injustificable; alterar un registro constituye falsedad ideológica sin importar el fin."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I5",
            "texto": "Un pasajero olvida un smartphone de alta gama en tu unidad. Recuerdas con claridad que dicho usuario fue sumamente prepotente e insultante contigo durante el viaje. ¿Qué sucede comúnmente en el gremio?",
            "opciones": [
                "Muchos conductores optarían por retener el equipo como una lección de civismo o 'karma' para el pasajero.",
                "Lo reportan a la central, pero dilatan la entrega varios días como respuesta al maltrato recibido.",
                "Se entrega de forma intacta e inmediata al área de custodia; la rectitud no se condiciona por el comportamiento ajeno."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I6",
            "texto": "Consumiste una sola botella de cerveza durante una reunión familiar hace exactamente 4 horas. Tu turno inicia pronto y te sientes completamente sobrio. ¿Qué decisión tomas?",
            "opciones": [
                "Asisto a operar con total normalidad; una sola unidad de alcohol es metabolizada por completo en ese lapso.",
                "Utilizo enjuague bucal clínico y mentas de alta concentración para evitar lecturas dudosas u observaciones.",
                "Me declaro inacto ante la jefatura de operaciones; la política de tolerancia cero al alcohol exige honestidad radical."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I7",
            "texto": "Un pasajero habitual te solicita transportar una encomienda pequeña sin boleto ni registro a cambio de un pago en efectivo equivalente a la mitad de la tarifa oficial. ¿Qué haces?",
            "opciones": [
                "Acepto el envío; el espacio en el maletero está disponible y no genera ningún perjuicio real a la operación.",
                "Comparto el beneficio económico con mi copiloto o ayudante de ruta para mantener un control interno del viaje.",
                "Rechazo la solicitud de inmediato; transportar elementos fuera de manifiesto es una falta grave de seguridad."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I8",
            "texto": "Por un error del sistema administrativo, la empresa omitió descontarte los días correspondientes a una suspensión previa. ¿Cómo actúas?",
            "opciones": [
                "Permanezco en silencio; los errores de los sistemas internos de la empresa son responsabilidad de la administración.",
                "Espero a que el departamento de contabilidad lo note por su cuenta en las auditorías de fin de año.",
                "Notifico la anomalía por escrito a Recursos Humanos para que realicen la corrección de haberes respectiva."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I9",
            "texto": "Detectas que un compañero con graves problemas económicos está retirando repuestos y consumibles del almacén central sin la autorización debida. ¿Cuál es tu postura?",
            "opciones": [
                "No intervengo; denunciar a un compañero en situación de vulnerabilidad destruye la cohesión interna del grupo.",
                "Hablo a solas con él para persuadirlo de que devuelva lo retirado antes de que las cámaras lo delaten.",
                "Informo de forma confidencial a la gerencia de riesgos; tolerar el hurto desfalca los recursos del proyecto común."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I10",
            "texto": "Un usuario te ofrece una gratificación económica significativa para que realices una parada en una zona prohibida pero que le resulta sumamente conveniente y segura para él. ¿Qué haces?",
            "opciones": [
                "Accedo a la parada si confirmo de forma visual que no hay inspectores de tránsito ni patrullas en las cercanías.",
                "Accedo únicamente si el pasajero demuestra una condición especial de vulnerabilidad (ej. fatiga extrema).",
                "Niego la parada de forma tajante; alterar los puntos aprobados rompe los protocolos de seguridad vial de la ruta."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I11",
            "texto": "Olvidaste registrar los datos técnicos de los últimos 3 días en la bitácora obligatoria. ¿Cómo solucionas este descuido documental?",
            "opciones": [
                "Completo los casilleros vacíos con estimaciones aproximadas basándome en mi memoria operativa.",
                "Lleno la bitácora replicando con exactitud los datos del promedio de la semana anterior para uniformizar.",
                "Asumo la omisión ante mi supervisor y procedo a reconstruir los datos basándome estrictamente en el GPS."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "I12",
            "texto": "¿Qué opinión te merece el uso ocasional de las instalaciones, herramientas y gatas hidráulicas de la empresa para realizar el mantenimiento preventivo de tu vehículo particular?",
            "opciones": [
                "Es una práctica aceptable siempre que se efectúe fuera de las jornadas laborales y con herramientas propias.",
                "Es tolerable si se cuenta con la autorización verbal del mecánico de turno o un operario de confianza.",
                "Es un uso indebido de los activos corporativos y constituye una infracción ética de apropiación ilícita."
            ],
            "puntajes": [0, 10, 20]
        }
    ],
    "Estabilidad Emocional y Trabajo Bajo Presión": [
        {
            "id": "E1",
            "texto": "Un conductor de transporte informal te cierra el paso de forma violenta e intencional para arrebatarte un pasajero en paradero. Tienes usuarios a bordo. ¿Cuál es tu respuesta inmediata?",
            "opciones": [
                "Acelero para ponerme a su nivel en el siguiente semáforo e increparle enérgicamente su maniobra criminal.",
                "Utilizo la bocina de forma prolongada e intensa para evidenciar su imprudencia ante los pasajeros y peatones.",
                "Freno a fondo resguardando la estabilidad, modulo mi respiración y mantengo distancia defensiva sin engancharme."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E2",
            "texto": "Un usuario descontento te insulta a gritos frente a todo el minibus debido a un retraso severo provocado por un choque ajeno en la vía. ¿Cómo gestionas la agresión?",
            "opciones": [
                "Le respondo con tono fuerte y autoritario para marcar límites firmes y no perder el control frente al grupo.",
                "Detengo por completo el vehículo y le exijo que abandone la unidad inmediatamente por perturbar el orden.",
                "Mantengo un silencio profesional absoluto, asimilo el malestar con madurez y aplico el protocolo con tono neutro."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E3",
            "texto": "Te asignan una unidad con el aire acondicionado inoperativo y un asiento con fallas de ergonomía en la jornada con mayor temperatura del año. ¿Qué efecto tiene esto en tu conducción?",
            "opciones": [
                "Incrementa mi nivel de frustración, induciéndome involuntariamente a conducir más rápido para concluir.",
                "Afecta significativamente mi confort, restándome capacidad de atención frente a los estímulos de la carretera.",
                "Es un factor adverso incómodo, pero logro blindar por completo mi rendimiento técnico y paciencia al volante."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E4",
            "texto": "Un mando medio te recrimina de forma airada y con términos ofensivos a través de la frecuencia radial abierta por una supuesta demora. ¿Cómo reaccionas?",
            "opciones": [
                "Le respondo con la misma intensidad y argumentos por el canal de radio para salvaguardar mi dignidad laboral.",
                "Apago el equipo de comunicación de forma temporal para evitar escuchar los agravios y estabilizar mi ritmo cardiaco.",
                "Emito un escueto 'Recibido, base', continúo enfocado en la ruta y solicito una reunión formal de descargos al llegar."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E5",
            "texto": "¿Cuál de las siguientes afirmaciones define con mayor realismo tu visión sobre la conducción en el tráfico pesado de las horas punta?",
            "opciones": [
                "Es un entorno hostil donde impera la ley de la fuerza; si no eres agresivo y cierras espacios, la operación fracasa.",
                "Es una situación estresante que obliga al piloto a emplear ciertas cuotas de viveza criolla para cumplir los horarios.",
                "Es un escenario de alta volatilidad de riesgo que demanda un control emocional riguroso y conducción 100% defensiva."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E6",
            "texto": "Un pasajero en evidente estado de ebriedad comienza a hostigar verbalmente e incomodar a los demás ocupantes del minibus. ¿Cómo intervienes?",
            "opciones": [
                "Me desplazo hacia los asientos traseros para confrontarlo verbal o físicamente y forzarlo a guardar compostura.",
                "Evito intervenir directamente mientras el altercado no afecte mi integridad física o la zona de conducción.",
                "Estaciono el minibus en un sitio seguro, calmo a los pasajeros y solicito la intervención de serenazgo o policía."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E7",
            "texto": "Un vehículo particular avanza sumamente lento obstruyendo tu carril en una vía rápida y se niega a ceder el paso. ¿Cómo procedes?",
            "opciones": [
                "Me coloco a escasos centímetros de su parachoques posterior (tailgating) para forzarlo por presión a orillarse.",
                "Efectúo ráfagas continuas de luces altas y toco la bocina de forma repetitiva hasta que decida cambiar de carril.",
                "Sostengo una distancia de amortiguación totalmente segura y aguardo con paciencia una oportunidad reglamentaria."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E8",
            "texto": "Minutos antes de encender el motor, recibes una llamada familiar con una mala noticia de alta carga emocional. ¿Qué curso de acción adoptas?",
            "opciones": [
                "Inicio la ruta procurando canalizar la angustia a través de una concentración rígida en la conducción técnica.",
                "Procedo a realizar el servicio tratando de evadir selectivamente el pensamiento para cumplir con mi turno programado.",
                "Informo de manera inmediata a mi supervisor mi inaptitud emocional transitoria para garantizar la seguridad vial."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E9",
            "texto": "Te equivocas de ramal en un tramo complejo y terminas perdiéndote. Los pasajeros notan el error y comienzan a proferir quejas airadas de inmediato. ¿Cómo respondes?",
            "opciones": [
                "Me irrito y les exijo silencio de forma imperativa argumentando que el estrés solo empeorará la situación.",
                "Sigo avanzando a velocidad sostenida esperando reubicarme visualmente de forma empírica en las siguientes calles.",
                "Detengo la marcha en zona segura, pido disculpas de manera calmada y utilizo el sistema de mapas o radio para reubicarme."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E10",
            "texto": "Con total sinceridad, ¿con qué frecuencia experimentas ira o frustración profunda hacia el comportamiento de los otros conductores en la ruta?",
            "opciones": [
                "Prácticamente a diario; el nivel de imprudencia e informalidad en las pistas es exasperante.",
                "Ocasionalmente, sobre todo cuando ejecutan maniobras temerarias que ponen en riesgo real a mi unidad.",
                "Casi nunca; entiendo el comportamiento ajeno como una condición ambiental fija de la ruta que exige tolerancia."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E11",
            "texto": "Tu copiloto comete un error grave de omisión informativa que altera la hoja de ruta y obligará a rehacer el reporte de fin de turno. ¿Cómo lo abordas?",
            "opciones": [
                "Le recrimino fuertemente su negligencia e incompetencia en ese instante delante de los pasajeros a bordo.",
                "Le manifiesto mi descontento con comentarios sarcásticos e ironías pesadas durante el resto del recorrido.",
                "Mantengo la serenidad operativa y espero a la conclusión del servicio para desglosar el error técnico en privado."
            ],
            "puntajes": [0, 10, 20]
        },
        {
            "id": "E12",
            "texto": "La junta directiva de la operación implementa de forma sorpresiva un nuevo paquete de normas de control de tiempos sumamente restrictivo. ¿Cuál es tu reacción?",
            "opciones": [
                "Me opongo abiertamente y busco aliarmarme con otros pilotos para resistir la aplicación de las normas.",
                "Acepto las disposiciones de mala gana, aplicándolas con desgano bajo protesta pasiva en mi día a día.",
                "Analizo los nuevos indicadores de control y me adapto con rapidez entendiendo las variaciones logísticas."
            ],
            "puntajes": [0, 10, 20]
        }
    ]
}

# ==============================================================================
# CONFIGURACIÓN DE LA INTERFAZ DE STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Evaluación Avanzada Midot - Pilotos", 
    layout="centered", 
    page_icon="🚦"
)

st.title("🚦 Sistema Avanzado de Evaluación de Conductores")
st.markdown("""
Este aplicativo evalúa de forma profunda el perfil psicométrico operativo y la confiabilidad 
de los pilotos de minibus bajo metodologías internacionales de análisis de riesgos críticos, 
integridad y toma de decisiones en entornos de alta presión.
""")

# ==============================================================================
# SELECCIÓN Y CONFIGURACIÓN DEL BANCO DINÁMICO DE PREGUNTAS (30 ÍTEMS)
# ==============================================================================
if 'preguntas_seleccionadas' not in st.session_state:
    st.session_state.start_time = time.time()
    
    seleccion = []
    # Balanceo riguroso: 8 de Seguridad, 8 de Fatiga, 7 de Integridad y 7 de Estabilidad = 30 preguntas
    seleccion.extend(random.sample(banco_preguntas["Seguridad y Riesgos Críticos"], 8))
    seleccion.extend(random.sample(banco_preguntas["Gestión de la Fatiga y Somnolencia"], 8))
    seleccion.extend(random.sample(banco_preguntas["Integridad y Cumplimiento Ético"], 7))
    seleccion.extend(random.sample(banco_preguntas["Estabilidad Emocional y Trabajo Bajo Presión"], 7))
    
    # Aleatorizar el orden general de aparición para cruzar rubros y evaluar consistencia cognitiva
    random.shuffle(seleccion)
    st.session_state.preguntas_seleccionadas = seleccion

# ==============================================================================
# RENDERIZADO DEL FORMULARIO EVALUATIVO
# ==============================================================================
with st.form("eval_form_avanzado"):
    st.warning("⚠️ Todas las situaciones planteadas requieren una respuesta obligatoria. Responda con base en el criterio profesional real.")
    
    for idx, p in enumerate(st.session_state.preguntas_seleccionadas):
        st.markdown(f"**Cuestión {idx+1}:** {p['texto']}")
        st.radio(
            label=f"Selección para {p['id']}:",
            options=p['opciones'],
            key=p['id'],
            label_visibility="collapsed"
        )
        st.divider()

    submit = st.form_submit_button("Concluir y Procesar Evaluación")

# ==============================================================================
# PROCESAMIENTO ANALÍTICO DE LOS RESULTADOS
# ==============================================================================
if submit:
    puntaje_total = 0
    puntaje_maximo = 30 * 20  # 30 ítems x 20 puntos de control óptimo = 600 puntos

    for p in st.session_state.preguntas_seleccionadas:
        respuesta_usuario = st.session_state[p['id']]
        indice_respuesta = p['opciones'].index(respuesta_usuario)
        puntaje_obtenido = p['puntajes'][indice_respuesta]
        puntaje_total += puntaje_obtenido

    porcentaje_final = round((puntaje_total / puntaje_maximo) * 100, 2)
    tiempo_total = round(time.time() - st.session_state.start_time, 2)
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)

    st.header("📊 Dictamen del Perfil Evaluado")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Índice de Confiabilidad Operativa", f"{porcentaje_final}%")
    with col2:
        st.metric("Tiempo de Resolución Psicométrica", f"{minutos} min {segundos} seg")
        
    st.divider()
    
    # Análisis de Desempeño según Rangos de Control de Pérdidas e Integridad
    if porcentaje_final >= 85:
        st.success("""
        ✅ **APTO - RECOMENDACIÓN ALTA (Alineamiento Preventivo Óptimo):**
        El evaluado demuestra una internalización profunda de los controles críticos de seguridad, 
        rechazo sistemático a la normalización del riesgo operativo y una sólida estructura ética. 
        Posee el criterio analítico necesario para operar unidades de transporte de pasajeros.
        """)
    elif porcentaje_final >= 65:
        st.warning("""
        ⚠️ **APTO EN OBSERVACIÓN - RECOMENDACIÓN RESTRINGIDA:**
        El evaluado presenta un perfil pragmático. Si bien conoce las normas, tiende a justificar la omisión 
        de controles menores bajo escenarios de alta presión del cliente o retrasos logísticos. 
        Se sugiere un plan de mentoría en HSEQ enfocado en Fatiga e IPERC Continuo antes de su liberación a ruta.
        """)
    else:
        st.error("""
        ❌ **NO APTO - ALTO RIESGO OPERATIVO CRÍTICO:**
        Las respuestas evidencian una marcada tendencia a la normalización de desvíos conductuales, 
        justificación de conductas de riesgo y debilidad frente a la deseabilidad social. Alta probabilidad 
        de verse involucrado en incidentes viales por negligencia o fatiga no controlada. No se recomienda su contratación.
        """)

# ==============================================================================
# CONTROL DE RESET DE LA APLICACIÓN (FUERA DEL FORMULARIO)
# ==============================================================================
st.markdown("---")
if st.button("🔄 Inicializar Nueva Evaluación (Reset)"):
    if 'preguntas_seleccionadas' in st.session_state:
        del st.session_state.preguntas_seleccionadas
    st.rerun()
