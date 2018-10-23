Export Invoices to Sistema TS
=============================

Export a number of invoices in a XML format suitable for Italian 'Sistema Tessera Sanitaria (TS)'.

Questo modulo aggiunge:

* un campo sul prodotto, per indicare il tipo di spesa;
* due campi sul cliente, uno per il codice fiscale criptato e uno per l'eventuale opposizione del cliente alla dichiarazione 730
* Una voce di menù "Invii 730"
* Una voce di menù "Encrypt fiscal codes" (in teoria inutile)

Utilizzo
--------

* Occorre ottenere password e pincode [2]
* (Teoricamente superfluo) Per criptare i codici fiscali, usare la voce di menù "Encrypt fiscal codes" (anche se in teoria a ogni modifica del codice fiscale dovrebbero criptarsi automaticamente il processo di criptatura).
* Esportare le fatture in formato XML tramite l'apposita Azione, selezionando le fatture del mese
* Andare nel menù Esportazioni TS e scegliere l'Azione "invia"


Ho riscontrato problemi con i certificati SSL del server, nel caso eseguire prima export PYTHONHTTPSVERIFY=0
(ignora tutti i certificati SSL...)

Stato dell'arte
---------------
**Il formato del file XML è estremamente limitato, e' stato testato solo per gli psicologi privati**

Note tecniche
-------------
Questo modulo utilizza zeep [3] come client SOAP, da installare con pip install zeep.


[1] https://sistemats1.sanita.finanze.it/portale/invio-telematico-documenti-e-specifiche-tecniche

[2] https://sistemats4.sanita.finanze.it/simossHome/login.jsp

[3] https://python-zeep.readthedocs.io/en/master/

