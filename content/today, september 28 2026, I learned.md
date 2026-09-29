---
tags:
  - evergreen
  - til
draft: false
created: 2026-09-28T21:42
modified: 2026-09-29T00:47
---
*an exercise in [[📕 Make it Stick|retrieval, reflection, generation, and elaboration]].*
# today I learned:

## about [[frontend web dev]] with [[MUI]] and [[React]] 
*from CodeHouse Front End Dev w/ Agentic AI Bootcamp week 2*
what I learned:
> * how to set up a React project with [Vite](https://vite.dev/guide/)
> * using ||`rafce` (**r**eact **a**rrow **f**unction **c**omponent with a default **e**xport)|| to create boilerplate code snippet
> * adding [[fonts]] with [fontsource](https://fontsource.org)
> * adding basic MUI elements like Button, TextField, and Typography

connections to prior knowledge/experience:
> * there seem to be a lot of similarities in the structure of the `App.tsx` file of a React project and the `ContentView.swift` file of a [[SwiftUI]] project
>```typescript
>	// a function React calls ||every time it renders||
>	const App = () => {
>		// initialize constants, variables, state variables, etc
>		return (
>			// page contents (explictly returned as ||some jsx||)
>		)
>	}
>```
>```swift
>	struct ContentView: View {
>		// initialize constants, variables, state variables, etc
>		var body: some View { // a computed property read ||whenever state changes||
>			// view contents (implicitly returns some kind of View)
>		}
>	}
>```
* do these similarities apply to all components in React and views in SwiftUI? --> ||yes||

gaps in knowledge/ability and lingering questions:
> * arrow functions in [[TypeScript]]:
> 	* what are they?
> 	* what are the alternative(s)?
> * how does React render components?

strengths:
> * I am comfortable setting up the dev environment & project
> * I am starting to recognize similarities between UI frameworks (React and SwiftUI)
> * I am comfortable reading MUI documentation to find the components I want to use and figure out how to use them


areas for improvement:
> * Im not very comfortable creating and using variables
> * Im not very comfortable using MUI component props and general web styling