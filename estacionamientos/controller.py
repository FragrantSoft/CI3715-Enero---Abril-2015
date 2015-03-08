# Archivo con funciones de control para SAGE
from estacionamientos.models import Estacionamiento
from datetime import datetime, timedelta, time

# chequeo de horarios de extended
def HorarioEstacionamiento(HoraInicio, HoraFin):
	return HoraFin > HoraInicio

def validarHorarioReserva(inicioReserva, finReserva, apertura, cierre):
	if inicioReserva >= finReserva:
		return (False, 'El horario de inicio de reservacion debe ser menor al horario de fin de la reserva.')
	if finReserva - inicioReserva < timedelta(hours=1):
		return (False, 'El tiempo de reserva debe ser al menos de 1 hora.')
	if inicioReserva.date() < datetime.now().date():
		return (False, 'La reserva no puede tener lugar en el pasado.')
	if finReserva.date() > (datetime.now()+timedelta(days=6)).date():
		return (False, 'La reserva debe estar dentro de los próximos 7 días.')
	if apertura.hour==0 and apertura.minute==0 \
		and cierre.hour==23 and cierre.minute==59:
		seven_days=timedelta(days=7)
		if finReserva-inicioReserva<=seven_days :
			return (True,'')
		else:
			return(False,'Se puede reservar un puesto por un maximo de 7 dias.')
	else:
		delta =       timedelta(hours=cierre.hour,  minutes=cierre.minute)
		delta = delta-timedelta(hours=apertura.hour,minutes=apertura.minute)

		if finReserva-inicioReserva>delta:
			return (False, 'El horario de inicio de reserva debe estar en un horario válido.')
		else:
			hora_inicio = time(hour = inicioReserva.hour, minute = inicioReserva.minute)
			hora_final  = time(hour = finReserva.hour   , minute = finReserva.minute)
			if hora_inicio<apertura:
				return (False, 'El horario de inicio de reserva debe estar en un horario válido.')
			if hora_final > cierre:
				return (False, 'El horario de fin de la reserva debe estar en un horario válido.')
		return (True,'')

def marzullo(idEstacionamiento, hIn, hOut):
	e = Estacionamiento.objects.get(id = idEstacionamiento)
	ocupacion = []
	capacidad = e.nroPuesto

	for reserva in e.reserva_set.all():
		ocupacion += [(reserva.inicioReserva, 1), (reserva.finalReserva, -1)]
	ocupacion += [(hIn, 1), (hOut, -1)]

	count = 0
	for r in sorted(ocupacion):
		count += r[1]
		if count > capacidad:
			return False
	return True

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip
