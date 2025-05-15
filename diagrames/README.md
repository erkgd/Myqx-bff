# Diagrames d'Arquitectura Myqx-BFF

Aquest directori conté els diagrames PlantUML que representen l'arquitectura del projecte Myqx-BFF (Backend For Frontend).

## Diagrames Disponibles

1. **estructura-general.puml**: Visió general de tota l'arquitectura Myqx-BFF i les seves capes.

2. **vistes-i-processament.puml**: Diagrama detallat de la capa de vistes API i el processament de peticions.

3. **controladors-i-vistes.puml**: Diagrama que mostra les relacions entre les vistes API i els controladors.

4. **serveis-i-interficies.puml**: Diagrama detallat dels serveis, les seves implementacions i interfícies.

5. **repositoris-dtos-models.puml**: Diagrama de la capa d'accés a dades, DTOs i models.

6. **utils-i-configuracio.puml**: Diagrama dels components d'utilitat, gestió d'excepcions i configuració.

7. **flux-peticions.puml**: Diagrama de seqüència que mostra el flux complet d'una petició des del client fins a la resposta.

## Configuració d'Estil

El fitxer `style-config.puml` conté la configuració d'estil comuna per a tots els diagrames. 
Aquest fitxer és inclòs en tots els diagrames per assegurar una aparença consistent.

## Com Visualitzar els Diagrames

Els diagrames es poden visualitzar amb qualsevol eina compatible amb PlantUML:

1. **Extensions de VS Code**: Instal·lar l'extensió PlantUML per visualitzar els diagrames directament a VS Code.
2. **Navegador Web**: Utilitzar el [Servidor Web PlantUML](http://www.plantuml.com/plantuml/uml/).
3. **Línia de Comandes**: Utilitzar l'executable de PlantUML per generar imatges.

```bash
java -jar plantuml.jar estructura-general.puml
```

## Actualització dels Diagrames

Els diagrames estan actualitzats a 14 de Maig, 2025. Quan es facin canvis significatius en l'arquitectura, caldrà actualitzar els diagrames corresponents.

## Llegenda de Colors

- <span style="background-color:#C2E0FF">■</span> Client
- <span style="background-color:#D5E8D4">■</span> Vistes API
- <span style="background-color:#DAE8FC">■</span> Controladors
- <span style="background-color:#FFF2CC">■</span> Interfícies
- <span style="background-color:#F8CECC">■</span> Serveis
- <span style="background-color:#FFE6CC">■</span> Repositoris
- <span style="background-color:#E1D5E7">■</span> DTOs
- <span style="background-color:#F5F5F5">■</span> Models
- <span style="background-color:#FFF8DC">■</span> Utils i Excepcions
- <span style="background-color:#D4E1F5">■</span> Middleware
