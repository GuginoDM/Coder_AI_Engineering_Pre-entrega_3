# Manual de Despliegue de Servicios en la Nube

## Procedimiento de Rollback
En caso de detectar una falla crítica durante la ventana de mantenimiento de un despliegue, el equipo debe ejecutar el script `rollback_deploy.sh` en el servidor principal.

## Notificaciones de Incidentes
Todo incidente clasificado como Severidad 1 (Pistas caídas o interrupción total del servicio) debe ser notificado de inmediato mediante el canal de Teams `#alertas-infra` en un lapso no mayor a 15 minutos de haber sido detectado.