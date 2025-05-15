# Diagrames d'Arquitectura Myqx-BFF (Versió Simplificada)

Aquest directori conté els diagrames PlantUML simplificats que representen l'arquitectura del projecte Myqx-BFF.

## Diagrames Simplificats

1. **estructura_general_simple.puml**: Visió general de tota l'arquitectura Myqx-BFF i les seves capes.

2. **vistes_i_processament_simple.puml**: Diagrama de la capa de vistes API i el processament de peticions.

3. **controladors_i_vistes_simple.puml**: Diagrama de les relacions entre les vistes API i els controladors.

4. **serveis_i_interficies_simple.puml**: Diagrama dels serveis, les seves implementacions i interfícies.

5. **repositoris_dtos_models_simple.puml**: Diagrama de la capa d'accés a dades, DTOs i models.

6. **utils_i_configuracio_simple.puml**: Diagrama dels components d'utilitat, gestió d'excepcions i configuració.

7. **flux_peticions_simple.puml**: Diagrama de seqüència que mostra el flux d'una petició.

8. **index_simple.puml**: Índex dels diagrames simplificats.

## Estil dels Diagrames

Els diagrames utilitzen un estil més simple i net amb les següents característiques:

- Ús de `skinparam packageStyle rectangle`
- Ús de `skinparam componentStyle uml2`
- Línies ortogonals amb `skinparam linetype ortho`
- Notes explicatives en lloc de llegendes complexes
- Components representats com [Component] en lloc de "Component"

## Com Visualitzar els Diagrames

Els diagrames es poden visualitzar amb qualsevol eina compatible amb PlantUML:

1. **Extensions de VS Code**: Instal·lar l'extensió PlantUML per visualitzar els diagrames directament a VS Code.
2. **Navegador Web**: Utilitzar el [Servidor Web PlantUML](http://www.plantuml.com/plantuml/uml/).
3. **Línia de Comandes**: Utilitzar l'executable de PlantUML per generar imatges.

```bash
java -jar plantuml.jar estructura_general_simple.puml
```

## Actualització dels Diagrames

Els diagrames estan actualitzats a 14 de Maig, 2025.
