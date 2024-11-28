# Tutkimus tavaran vastaanottamisesta varastolla - Koivunen Oy
![image](https://github.com/pyrypp/koivunen-vastaanottoanalyysi/assets/120693130/e7686b82-2193-4380-adcd-ade20b0386f6)


Koivusen logistiikkapäällikön pyynnöstä toteutetussa tutkimuksessa tutkitaan Koivunen Oy:n varastolle saapuvaa tavaraa. Logistiikkapäällikön ongelma oli, että varastolle kasautuu enemmän tavaraa kuin työntekijät ehtivät laittaa hyllyyn. Siis:
- Miksi varastolla on kiirettä?
- Mitä muutoksia varaston toiminnassa on tapahtunut?
- Miten eri muuttujat vaikuttavat tavaran käsittelynopeuteen?

Sain dataa analysoitavaksi ja kahlasin sitä läpi logistiikkapäällikön toiveiden mukaisesti.

Tutkimuksen tulokset on esitetty interaktiivisessa muodossa osoitteessa: 
https://pyryp-koivunen-vastaanotto-dataesitys.streamlit.app/

Logistiikkapäällikön mukaan tutkimus tuki varaston johdon päätöksentekoa ja antoi dataan pohjautuvan vahvistuksen aikaisemmille arvioille. Logistiikkapäällikkö lähti lopulta ratkomaan ongelmaa muun muassa uusien työaikajärjestelyjen avulla.

_Kuva: Koivunen Oy_
##
[![image](https://github.com/user-attachments/assets/03a1ae2e-fed5-47c7-bfb6-3938cbac8309)](https://pyryp-koivunen-vastaanotto-dataesitys.streamlit.app/)

## Mitä opin?
- Data-analyysiä Pythonilla
  - Taulukkodatan käsittelyä (Pandas)
  - Epätäydellisen datan siistimistä (data cleansing, NaN-arvot)
  - Datan eksploratiivista tutkimista Pandasin ja Plotlyn avulla
  - Regressiokäyrien sovittaminen (Scipy)
  - Feature engineering
  - Datetime-arvot ja ryhmittely niiden mukaan
- Todellisen liiketoimintaongelman ratkomista todellisella datalla
  - Kommunikointi päätöksentekijöiden kanssa
- Tulosten esittäminen interaktiivisesti nettisivun avulla
  - Streamlit
  - Visualisointien kustomointimahdollisuus
  - Tuloksista ja niiden tulkinnasta selkeästi viestiminen
