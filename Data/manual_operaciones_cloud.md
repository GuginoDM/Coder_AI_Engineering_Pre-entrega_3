# Manual de Operaciones e Infraestructura Cloud

Documentación Técnica para Ingeniería y DevOps.

## 1. Arquitectura de Despliegue y CI/CD

Los despliegues de microservicios en la nube de producción se gestionan mediante **ArgoCD** y **GitOps**. Los componentes principales están orquestados sobre un clúster de **Kubernetes (EKS)** distribuido en tres zonas de disponibilidad (`AWS us-east-1`).

### Estrategia de Despliegue Canary
Todo cambio en el código fuente que sea fusionado en la rama `main` de GitHub desencadena una canalización automática en GitHub Actions. La estrategia predeterminada es un despliegue Canary:
- El nuevo contenedor recibe inicialmente el **10% del tráfico durante 15 minutos**.
- Se monitorean métricas de error (HTTP 5xx) y latencia (p99).
- Si el porcentaje de errores es inferior al **0.05%**, la versión se promociona automáticamente al 100% del clúster.

## 2. Procedimiento de Rollback de Emergencia

En caso de que un nuevo despliegue genere degradación en los servicios de producción y las métricas automáticas no detengan la promoción, se debe ejecutar el rollback manual inmediato.

### Pasos de Rollback:
1. Conectarse al clúster mediante la CLI utilizando el rol de emergencia de DevOps:
   ```bash
   aws eks update-kubeconfig --region us-east-1 --name prod-cluster-main