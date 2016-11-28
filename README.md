# Projet compilateur

## Interpréteur de pseudo-code

Le but de notre projet est de créer un interpréteur de pseudo code.

### Exemple de code

```
fonction main()
debut
  variable V = 1
  affiche V
  si V > 2 alors
    dec V
  finsi

  variable T = 0
  tant que T < 10 faire
    affiche T
    inc T
  fintantque

  appelle test(10)

finfonction

fonction test(variable A)
debut
  affiche A
fin
```

Sortie de ce code:

```
1
0
1
2
3
4
5
6
7
8
9
10
```

### Techniques et contraintes

* Le projet sera réalisé en Python à l'aide de la bibliothèque _PLY_
* Le projet doit impérativement passer par la construction d'un arbre syntaxique.
* Le projet devra être conçu pour que les étapes intermédiaires du traitement soient facilement accessibles.
