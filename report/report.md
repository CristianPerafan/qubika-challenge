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

Diagrama de la arquitectura del sistema:

![Arquitectura del Sistema](./img/diagram.png)

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

Diagrama del proceso de *scraping*:

![Proceso de Scraping](./img/scraping.png)

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
(*Large Language Model*, LLM) de *OpenAI* (*gpt-4o*), asistido por el contexto adicional extraído de la base 
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

   Ejemplo de consulta: *¿Puedes comparar las noticias tituladas "Preocupa Ecopetrol" (publicada por El Tiempo) y 
   "Corrupción en Ecopetrol para pagar favores de campaña: Audio vincula a amigo de Petro y al presidente de Cenit" 
   (publicada por La Silla Vacia), analizando las perspectivas, enfoques y posibles sesgos editoriales de cada medio?*
    
    De la anterior consulta se extraen los siguientes elementos:
    ```json
    {
        "titulos": [
            "Preocupa Ecopetrol",
            "Corrupción en Ecopetrol para pagar favores de campaña: Audio vincula a amigo de Petro y al presidente de Cenit"
        ],
        "fuentes": [
            "El Tiempo",
            "La Silla Vacia"
        ]
    }
    ```
   
    Con esta información, el sistema puede realizar una búsqueda más precisa en la base de datos vectorial, recuperando
    los fragmentos de texto correspondientes a cada noticia y proporcionando un análisis comparativo más detallado.


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
Las pruebas se realizarón utilizando `DeepEval`, se buscó evaluar la relevancia y correctitud de las respuestas generadas
por el sistema. Los resultados obtenidos fueron los siguientes:


### Test: Evaluación de Relevancia de la Respuesta Generada

- **Descripción:** Este test evalúa la relevancia de las respuestas generadas por el modelo RAG en relación con el 
  contexto de recuperación.
- **Contexto:** El test fue realizado utilizando como referencia principal el artículo titulado *"Presidente Gustavo 
  Petro llegó a Brasil para participar de la cumbre del G20"*, publicado por *El Tiempo*.

### Test: Evaluación de Relevancia y Correctitud de la Respuesta Generada

- **Descripción:** Este test evalúa tanto la relevancia como la correctitud de las respuestas generadas por el modelo 
  RAG en relación con el contexto de recuperación y la precisión de los detalles proporcionados.
- **Contexto:** El test fue realizado utilizando como referencia principal el artículo titulado 
  *"Presidente Gustavo Petro llegó a Brasil para participar de la cumbre del G20"*, publicado por *El Tiempo*.

### **Resultados del Test:**
1. **Relevancia:**
   - **Métrica evaluada:** Relevancia de la respuesta.
   - **Puntuación obtenida:** 0.56 (umbral: 0.5).  
     La respuesta contiene información relevante sobre el propósito principal de la cumbre del G20, aunque incluye 
     secciones que no abordan directamente este propósito, como un resumen más amplio y detalles específicos no 
     relacionados.

2. **Correctitud:**
   - **Métrica evaluada:** Correctitud de la respuesta.
   - **Resultado:** La respuesta generada contiene información precisa y coherente con el contenido del artículo de 
     referencia.

**Captura de Pantalla del Resultado:**
![Resultados del Test](./img/test.png)



