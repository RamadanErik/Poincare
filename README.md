# Program működése:

## Bemeneti paraméterek:

A kód elején lévő bemeneti paramétereket kell változtatni, ha más szimulációt akarunk, ezen bemenetek a következők:
* _hiba1, hiba2, hiba3_  --- A három waveplate eltérése az ideális λ/4-es, λ/2-es és λ/4-estől sorban.
* _felbontás_ --- A random elforgatásokkal generált pontok száma a gömbön.
* _pontossag_ --- A random (egyenletes eloszlású) tesztpontok száma a gömbön.
* _tűréshatár_ --- A tesztpontoktól és a generált pontok közötti legnagyobb elfogadott távolság.
* _fény_ --- A bemeneti fény polarizációja.

## Pontok generálása:
A pontokat úgy generáljuk, hogy a bemenő fényre hattatjuk a három "waveplate"-et, melyeknek vízszintestől való elforgatását random generáljuk, ideálístól való eltérésüket, pedig a _hiba_ változókkal állíthatjuk be.
(A generált pontok számát az előbb megadott _felbontás_ változóval állíthatjuk be.)

## Megjelenítés:
A megjelenítéshez egy _"numpy array"_-ban elmentjük a legenerált pontok _Stokes-paramétereit_ (S0,S1,S2,S3), majd az első paraméterrel lenormálva a másik hármat ábrázoljuk 3 dimenziós _descartes-féle_ koordinátarendszerben.
A könnyebb átláthatóság érdekében egy szürke egység sugarú gömböt is ábrázolunk, melynek felszínén található az összes teljesen polarizált fény által reprezentált pont.

## Gömbfelszín lefedettségének tesztelése:
A gömbfelszín lefedettségének tesztelésére, azaz a 3 _"waveplate"_ együttes működésének értékelésére, tesztpontokat generálunk a gömbfelszínen egyenletes eloszlással és megnézzük, hogy található-e tőle egy bizonyos (tűréshatárnyi) távolságon belül generált pont. Összeszámolva az olyan pontokat, melyekre az előbbi teljesül és elosztva a tesztpontok számával (pontosság), százalékos lefedettségi értéket kapunk.
