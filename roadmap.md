- [ ] Download per artist (fijarse en release 1.2)
- [ ] Releases: Windows Linux Mac
- [ ] Modos de uso e instalacion: 
	1. Un binario doble click linux y windows (carpeta releases/binaries) 
	1. Terminal: python3 programa -flags... etc
- [ ] Gifs de como usar 
- [ ] Esperando al user input -> Thread nuevo para ejecutar en el background
- [ ] Arg Parser:
	* command_line_arg
- [ ] Diccionario de flags y que todo reciba eso y diccionario de parametros
- [ ] Logging
- [ ] Buen project tagline

# Refactor
- [ ] SOLID -> Una responsabilidad, no depender de cosas concretas (como bases de datos especificas)
- [ ] Documentar y respetar contrato -> Firma, precondiciones, postcondiciones, invariantes
- [ ] Si no se cumplen las precondiciones al principio, lanzar excepcion
- [ ] Evitar muchos ifs -> polimorfismo
- [ ] Calcular todo lo posible preciclo
- [ ] Nombres de funciones son soluciones, no problemas
- [ ] Nombres de booleanos evaluando a true
- [ ] Metodos que NO usa el usuario -> _privados
- [ ] Las clases no funcionan como contenedores de datos, tienen que tener comportamiento independiente
- [ ] Capturar errores no genericos, todo tiene que estar controlado
- [ ] Muchos metodos similares, datos sueltos, codigo repetido -> hacer una clase nueva
- [ ] Minimo acoplamiento (interdependencia) posible
- [ ] Sin prints sueltos -> Todo print es seguido de algun return True/False o valor y/o es un logging
- [ ] Jetbrains inspect code
- [ ] https://refactoring.guru/refactoring y https://refactoring.guru/refactoring
