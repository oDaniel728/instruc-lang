# Instruc Lang

> Uma linguagem pequena, direta e experimental para brincar com stacks, comandos e mini-DSLs em Python.

Se voce curte construir linguagens, testar ideias de parser/runtime e ver tudo funcionando com sintaxe enxuta, esse projeto e para voce.

**O que voce encontra aqui:**
- runtime simples e extensivel
- bibliotecas nativas (`std`, `math`, `stacks`, `str`)
- testes `.instruc` prontos para estudar e evoluir
- docs tecnicas para entender e criar novas libs

## Exemplos rapidos

Rodar um exemplo pronto:

```bash
python main.py test/helloworld.instruc
```

Rodar com snapshot de debug:

```bash
python main.py test/helloworld.instruc --debug
```

Programa minimo em Instruc:

```instruc
new def @load
	req comments
	req std
end def

new def @main
	new stack $
	use stack $
		load 10
		load 20
		call std@print
	end stack *
end def

new def @quit
end def
```

Exemplo com string:

```instruc
new def @load
	req comments
	req std
	req str
end def

new def @main
	new stack $
	use stack $
		str concat "Instruc" " Lang" > $
		call std@printf
	end stack *
end def

new def @quit
end def
```

## Veja no GitHub

[github.com/oDaniel728/instruc-lang](https://github.com/oDaniel728/instruc-lang)

Abra o repo, rode os exemplos e comece a criar seus proprios comandos.
