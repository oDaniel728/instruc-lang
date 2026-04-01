# Tiny Update Showcase

Mini vitrine da atualização mais recente da Instruc Lang.

## Mini Changelog

### v1.1.0 (atual)

- novas libs: `builtins`, `ireq`, `read` e `epar`
- mais testes de cenários reais (`input`, import de arquivo e exemplos extras)
- snippets para acelerar criação de código Instruc e bibliotecas Python
- docs reorganizadas com 1 markdown por biblioteca em `docs/libs/`
- referência aprofundada de tipos/símbolos em `docs/types-protocols.md`

### v1.0.0 (base)

- commit de referência: `91cf15dbb38964799b3c999f933f02ff0b83420b`
- runtime base + bibliotecas principais + docs iniciais

## O que ficou legal nessa versão

- API de extensão mais clara para quem cria bibliotecas
- onboarding mais rápido via docs separadas por assunto
- exemplos de entrada/import para testar fluxo real de script

## Exemplos rápidos da atualização

### 1) Ler entrada tipada com `read`

```instruc
new def @load
    req str
    req read
    req std
end def

new def @main
    new stack $
    use stack $
        read int "Digite um número: "
        call std@print
    end stack *
end def
```

### 2) Importar outro `.instruc` com `ireq`

```instruc
new def @load
    req str
    req ireq
end def

new def @main
    ireq "./test/test_imports.instruc"
end def
```

### 3) Comando custom de exemplo com `epar`

```instruc
new def @load
    req epar
end def

new def @main
    epar 10
    epar 7
end def
```

## Rota de leitura recomendada

1. `README.md`
2. `docs/quickstart.md`
3. `docs/libs/README.md`
4. `docs/types-protocols.md`

## Rodando agora

```bash
python main.py test/helloworld.instruc
python main.py test/helloworld.instruc --debug
```
