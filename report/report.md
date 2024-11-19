# **Informe Certificación Qubika**

## **Introducción**

El presente informe tiene como objetivo describir, de manera detallada, el proceso de construcción de un sistema de 
*Retrieval-Augmented Generation* (RAG) diseñado para la generación de respuestas utilizando un Large Language Model 
**LLM**. Este sistema incorpora contexto adicional extraído de una base de datos vectorial que almacena documentos 
de noticias provenientes de dos reconocidos sitios web de noticias en Colombia: *El Tiempo* y *La Silla Vacía*. El 
proceso de extracción de noticias se realizó mediante *web scraping* y se almacenaron en una base de datos vectorial
(Chroma).

## **Arquitectura del Sistema**  

El sistema *Retrieval-Augmented Generation* (RAG) se compone de tres módulos principales: el módulo de *scraping*, 
el módulo de base de datos, el módulo de generación de respuestas y el módulo de la Interfaz de Usuario. 
A continuación, se describe en detalle cada uno de 
estos componentes.  

### **Módulo de *Scraping***  

El módulo de *scraping* tiene como objetivo principal la extracción de noticias desde los sitios web *El Tiempo* y 
*La Silla Vacía*. Para ello, se empleó la librería `BeautifulSoup` de Python, que facilita la obtención de datos 
estructurados desde páginas web.  

El proceso de *scraping* se organiza en dos funciones principales:  
1. La extracción de un número determinado de artículos de las secciones principales de los sitios web mencionados.  
2. La extracción específica del contenido de una noticia a través de una URL particular que pertenezca a uno de estos 
   medios.  

Para cada artículo procesado, se recopilan los siguientes datos:  
- **Título:** El encabezado de la noticia.  
- **Contenido:** El cuerpo principal de la noticia, obtenido mediante `BeautifulSoup` y posteriormente procesado con 
  la ayuda de un agente asistido por un LLM. Este agente utiliza el modelo *gpt-3.5-turbo-0125* de la plataforma 
- *OpenAI* para identificar y extraer el contenido más relevante.  
- **Fuente:** El medio de comunicación de origen de la noticia (*El Tiempo* o *La Silla Vacía*).  
- **URL:** La dirección web de la noticia.  
- **Fecha de Publicación:** La fecha en la que se publicó la noticia.  
- **Autor:** El nombre del autor de la noticia, cuando está disponible.  

### **Módulo de Base de Datos**  

Este módulo se encarga de almacenar y organizar la información extraída de las noticias en una base de datos vectorial. 
Se utilizó *Chroma*, una base de datos optimizada para el almacenamiento y recuperación eficiente de datos vectoriales.  

El procesamiento en este módulo incluye:  
1. **Conversión a vectores:** Cada noticia es transformada en vectores de alta dimensionalidad utilizando un modelo de 
   *embeddings*. Para este propósito, se empleó el modelo *text-embedding-3-large* de *OpenAI*.  
2. **Fragmentación del contenido:** Cada noticia se divide en fragmentos de texto de tamaño fijo mediante un proceso 
   conocido como *chunking*. Esto permite manejar de manera más eficiente la información en la base de datos vectorial. 
   Experimentalmente, se determinó que el tamaño óptimo de cada fragmento es de 800 caracteres.  

Estos fragmentos, representados como vectores, son almacenados en la base de datos para su posterior recuperación y uso 
en el sistema de generación de respuestas.  

### **Módulo de Generación de Respuestas**  

El módulo de generación de respuestas tiene como propósito procesar las consultas realizadas por el usuario y 
proporcionar respuestas coherentes y relevantes. Este módulo utiliza un modelo de lenguaje de gran escala 
(*Large Language Model*, LLM) de *OpenAI* (*gpt-3.5-turbo-0125*), asistido por el contexto adicional extraído de la base 
de datos vectorial.  

El flujo de trabajo de este módulo se estructura de la siguiente manera:  
1. **Procesamiento inicial de la consulta:**  
   Antes de realizar la búsqueda en la base de datos, se analiza la consulta del usuario para identificar si contiene 
   elementos específicos, como:  
   - **Títulos:** Indicaciones sobre el nombre de una noticia.  
   - **Autores:** Referencias a periodistas o escritores.  
   - **Fechas:** Indicaciones temporales relacionadas con la publicación de noticias.  

   Si se identifican uno o más de estos elementos, esta metainformación es utilizada para enriquecer y precisar la 
   consulta en la base de datos vectorial.  

2. **Búsqueda en la base de datos vectorial:**  
   - Cuando se dispone de metadatos (como los mencionados anteriormente), la búsqueda utiliza estos parámetros específicos.  
   - En caso de que no se detecten metadatos relevantes en la consulta, la búsqueda se realiza únicamente con la entrada 
     textual proporcionada por el usuario.  

3. **Generación de la respuesta:**  
   Una vez recuperada la información relevante desde la base de datos, esta se envía al LLM como contexto adicional. 
   El modelo genera una respuesta basada tanto en el contenido recuperado como en la consulta inicial del usuario, 
   asegurando que sea precisa, coherente y contextualizada.  

Este enfoque híbrido permite al sistema aprovechar tanto el poder generativo del LLM como la capacidad de recuperación 
precisa de información de la base de datos vectorial.  

### **Módulo de Interfaz de Usuario**
El módulo de Interfaz de Usuario (UI) es la interfaz gráfica que permite a los usuarios interactuar con el sistema.
La UI se construyo utilizando la librería `Streamlit` de Python, que facilita la creación de aplicaciones web interactivas.
En la UI, los usuarios pueden:
- Ingresar una consulta al agente RAG.
- Actualizar la base de datos con nuevas noticias.
- Agregar un artículo específico a la base de datos. El artículo debe pertenecer a uno de los medios de comunicación
  mencionados anteriormente.
- Visualizar las noticias disponibles en la base de datos.
- Reproducir por audio la respuesta generada por el agente RAG.

Es importante destacar que todos los módulos del sistema se construyeron utilizando `Langchain`, lo cual facilitó la
interacción entre los diferentes componentes y la integración de los modelos de *OpenAI*.

## **Pruebas y Resultados**

Para evaluar el desempeño del sistema, se realizaron pruebas de generación de respuestas utilizando `DeepEval`, una 
herramienta de evaluación de lenguaje natural. A continuación, se describen las dos pruebas principales realizadas:

### **Prueba de Relevancia de Respuestas**  
En esta prueba se evaluó si las respuestas generadas por el sistema son relevantes respecto a la consulta planteada 
por el usuario. Para ello, se utilizó la métrica **Answer Relevancy Metric**, la cual compara el contenido de la 
respuesta generada con el contexto proporcionado por la base de datos vectorial. El objetivo fue garantizar que las 
respuestas no solo fueran relacionadas temáticamente, sino también útiles para la consulta específica. Se definió un 
umbral de relevancia de 0.5 como criterio para considerar una respuesta aceptable.

### **Prueba de Exactitud de Respuestas**  
Esta prueba tuvo como propósito determinar si las respuestas generadas eran correctas respecto a la información 
contenida en la base de datos vectorial. Para ello, se utilizó la métrica de **Correctness** de `DeepEval`, que compara 
la respuesta generada con una salida esperada predefinida. La evaluación incluyó un análisis estricto, donde cualquier 
discrepancia entre la respuesta generada y la esperada era considerada como un fallo. Este enfoque permitió verificar 
que el modelo no solo ofreciera respuestas relevantes, sino que fueran precisas y consistentes con el contenido de los 
documentos extraídos.


