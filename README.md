# Proyecto QA para Urban Routes

## Descripción del Proyecto

Este proyecto está diseñado para automatizar las pruebas de la funcionalidad de solicitud de taxis en la aplicación Urban Routes. Las pruebas abarcan desde la configuración de direcciones de recogida y destino, la selección de tarifas, la introducción de información de contacto y tarjeta de crédito, hasta la verificación de la asignación de conductores. El objetivo es asegurar que cada paso en el proceso de solicitud de un taxi funcione correctamente y se manejen adecuadamente los datos ingresados por el usuario.

## Documentación

La fuente de documentación para este proyecto proviene de la especificación funcional de la aplicación Urban Routes. Esta documentación detalla las rutas y comportamientos esperados, los cuales se han utilizado para construir y validar las pruebas automatizadas.

## Tecnologías y Técnicas Utilizadas

- **Python**: Lenguaje de programación principal utilizado para implementar las pruebas automatizadas.
- **Selenium**: Herramienta utilizada para la automatización del navegador, permitiendo interactuar con la aplicación web como lo haría un usuario real.
- **Pytest**: Framework de pruebas utilizado para organizar y ejecutar pruebas automatizadas.
- **Git y GitHub**: Herramientas de control de versiones y colaboración para gestionar el código y el proyecto.

## Funcionalidades Implementadas

- **Configuración de Direcciones**: Función para establecer la dirección de recogida y destino en la aplicación.
- **Selección de Tarifa**: Automatización del proceso de selección de la tarifa de viaje (Comfort).
- **Ingreso de Información de Contacto**: Introducción y verificación del número de teléfono del usuario.
- **Adición de Tarjeta de Crédito**: Proceso automatizado para añadir la información de la tarjeta de crédito necesaria para solicitar un taxi.
- **Solicitudes Especiales**: Funcionalidad para enviar mensajes al conductor y solicitar artículos adicionales durante el viaje.
- **Asignación de Conductor**: Verificación de la correcta asignación de un conductor tras la solicitud del taxi.

## Instrucciones para Ejecutar las Pruebas

1. **Configuración del Entorno**: Asegúrate de tener Python y las bibliotecas necesarias (Selenium, Pytest) instaladas en tu entorno de desarrollo.
2. **Clonación del Repositorio**: Clona el repositorio en tu máquina local usando `git clone <URL del repositorio>`.
3. **Ejecución de Pruebas**: Navega al directorio del proyecto y ejecuta las pruebas utilizando el comando `pytest`.
