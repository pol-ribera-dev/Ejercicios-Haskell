# Analizador de tipos HinNer by Pol Ribera

Este proyecto implementa un analizador de expresiones utilizando Python y ANTLR. Está diseñado para parsear y analizar expresiones matemáticas y lógicas, identificar su tipo y representarlas gráficamente. La sintaxis que acepta este analizador es similar a la de Haskell ya que usa notación prefija y permite aplicaciones y abstracciones.  

## Requisitos
Para ejecutar este proyecto, necesitarás Python 3.8 o superior y ANTLR4. Además, asegúrate de tener instalados los siguientes paquetes:

- `antlr4-python3-runtime`
- `streamlit`
- `graphviz`
- `pandas`

Una vez que tengas todo instalado, ejecuta las siguientes instrucciones en el directorio donde tengas los archivos `hm.py` y `hm.g4`:
- `antlr4 -Dlanguage=Python3 -no-listener hs.g4`
- `antlr4 -Dlanguage=Python3 -no-listener -visitor hs.g4`
- `streamlit run hs.py`

Si se ha abierto una web en el navegador entonces todo ha ido perfecto. 

## Usabilidad

Una vez en la web encontrarás un campo de texto donde tienes que poner lo siguiente en este orden (en caso que no se haga así podrían surgir errores no contemplados): 
- Las declaraciones de tipo que quieras, con la forma `variable :: tipo` por ejemplo `x :: N -> N` (en el tipo no se pueden poner paréntesis, la asociatividad es siempre por la derecha). Se pide encarecidamente que no se defina dos veces la misma variable, ya que no tendría sentido y el código podría actuar de forma inesperada.
 
- Solamente una expresión tipo Haskell por ejemplo `\x -> (+) 2 x`

Una vez hayas insertado lo que desees pulsa `Ctrl + Enter` 



El resultado que se te mostrará será: 
- Un árbol de la expresión con los tipos correspondientes que habias definido. En caso de que aparezca algún átomo al cual no le hayas definido tipo se mostrará la variable que se le ha asignado.
- Un árbol de la expresión con la inferencia de tipos ya hecha, donde cada átomo ya tendrá su tipo corresponiente.
- Una tabla con todas las variables donde podrás observar su tipo y ver el resultado de la inferencia de tipos.
- Una última tabla donde se mostrarán las declaraciones hechas por el propio usuario. 
- Si hay algun error podrás ver en pantalla lo que lo ha generado.

## Explicación de las funciones del código

### posar_tipos
Recorre recursivamente el árbol de tipos que hemos generado con los visitadores de antlr4, y se encarga de poner el tipo corresponiente a los átomos que el usuario haya definido en la gramática. En el caso que el usuario no haya dicho de qué tipo quiere que sea este átomo, se le asignará una variable (letra minúscula).
### calcular_tipo
Se encarga de hacer la inferencia de tipos recursivamente. En el caso de las abstracciones usaremos `a = b → c`, así que solo podremos hacer la inferencia en el caso que sepamos `a` (asumiremos que `b` será de la forma N, siendo N el tipo de más a la izquierda de `a`, y que `c` será el resto de `a`)  o en el caso que sepamos `b` y `c` (simplemente haremos que `a` sea `b` -> `c`). Paralelamente en las aplicaciones usaremos `b = c → a`. Una vez acabada una inferencia, si hay algun valor que haya sido modificado, recorreremos otra vez su subárbol para asegurarnos que ese cambio no ha generado ningún error o para ver si ha desatascado la inferencia por allí. 
### arbol
De forma recursiva se recorre el árbol, generando así otro árbol creado en lenguaje Dot que después será el que se mostrará por pantalla. 