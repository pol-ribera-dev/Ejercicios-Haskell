grammar exprs;
root : 
     tipos EOF    #definicions 
     | terme EOF  #expresions  
     ;

terme:
      terme terme                                     #aplicacio
      | PARE terme PARD                               #parentesis
      | BARRITA ID FLEXITA terme                      #abstraccio
      | NUM                                           #numero
      | OP                                            #operador
      | ID                                            #id
;

tipos:
      (NUM | OP | ID) PUNTOS TYPE (FLEXITA TYPE)*
;


TYPE : ('A'..'Z');
PUNTOS : '::' ;
FLEXITA : '->';
OP : '(+)' | '(*)'  ;
BARRITA : '\\';
PARE : '(';
PARD : ')';
NUM : [0-9]+ ;
WS  : [ \t\n\r]+ -> skip ;
ID  : ('a'..'z'); 

     