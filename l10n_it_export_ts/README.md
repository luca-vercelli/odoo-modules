#Export Invoices to Sistema TS
Export a number of invoices in a XML format suitable for Italian 'Sistema Tessera Sanitaria (TS)'.

Questo modulo aggiunge:
* un campo sul prodotto, per indicare il tipo di spesa;
* due campi sul cliente, uno per il codice fiscale criptato e uno per l'eventuale opposizione del cliente alla dichiarazione 730
* Una voce di menù "Invii 730"
* Una voce di menù "Encrypt fiscal codes" (in teoria inutile)

##Utilizzo:
questo modulo permette l'esportazione in formato XML opportuno delle fatture, come se fosse un report.
Non esegue nè la compressione, nè l'invio.

Per criptare i codici fiscali, usare la voce di menù "Encrypt fiscal codes" (anche se in teoria a ogni modifica del codice fiscale
dovrebbero criptarsi automaticamente il processo di criptatura).

Per inviare il file, da riga di comando (Linux) modificare il file properties.py e lanciare lo script ./client.py

Ho riscontrato problemi con i certificati SSL del server, nel caso eseguire prima export PYTHONHTTPSVERIFY=0
(ignora tutti i certificati SSL...)

##Stato dell'arte:
Il formato del file XML è estremamente limitato, funziona solo per gli psicologi privati.

##Note
Questo modulo include una versione modificata di osa [2], che apparentemente non è più mantenuto.


[1] http://sistemats1.sanita.finanze.it/wps/content/Portale_Tessera_Sanitaria/STS_Sanita/Home/Sistema+TS+informa/730+-+Spese+Sanitarie/730+-+Spese+Sanitarie+-+Documenti+di+progetto+e+specifiche+tecniche/

[2] https://bitbucket.org/sboz/osa
