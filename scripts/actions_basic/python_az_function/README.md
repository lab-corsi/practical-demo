Vai su Settings > Secrets nel tuo repository e aggiungi i seguenti segreti:

- AZURE_CREDENTIALS: Questo è il file JSON delle credenziali di servizio di Azure che contiene le informazioni di accesso (puoi generarlo dal portale Azure, vedi sotto).
- AZURE_SUBSCRIPTION_ID: L'ID della tua sottoscrizione Azure.
- AZURE_TENANT_ID: L'ID del tenant Azure.
- AZURE_CLIENT_ID: L'ID del client (app registrata in Azure AD).
- AZURE_CLIENT_SECRET: Il segreto per l'app registrata (puoi ottenere questo segreto dal portale Azure).

`az ad sp credential reset --name <app-registration-name> --create-cert`

## host.json - Significato delle sezioni

`version`
Indica la major version del runtime Functions a cui si riferisce la sintassi (qui 2.x e 3.x).

`extensionBundle`
Specifica gli extension bundle (binding, trigger, ecc.) preinstallati, senza doverli elencare uno per uno.

`logging`

- `applicationInsights.samplingSettings` abilita il campionamento dei log per non sovraccaricare Insights.
- `logLevel` definisce il livello di severità di default e per categorie specifiche.

`functionTimeout`
Timeout massimo di esecuzione di una Function (formato HH:MM:SS). Se omesso, usa il default (230 secondi su consumption plan).

`http`

- `routePrefix` prefisso comune per tutti gli endpoint HTTP (es. api/).
- `maxOutstandingRequests`, `maxConcurrentRequests` limitano il numero di richieste in coda e in parallelo.

`watchDirectories`
Elenco di cartelle aggiuntive che, in local development, vengono ricontrollate per il reload automatico (es. SharedCode con moduli comuni).
