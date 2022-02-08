Application centralisant les actions à effectuer sur les données de l'inventaire. Déploiement à venir sur PythonAnyWhere pour une utilisation en production.

L'ensemble des données est soumis à divers droits.

Comptages dans la base:
```
echo "SELECT 'SELECT count(*), \"' || name || '\" FROM ' || name || ';'  FROM sqlite_master WHERE type = 'table';" | sqlite3 -readonly "$dbpath" | sqlite3 -readonly "$dbpath"
```
