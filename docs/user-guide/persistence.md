# Persistencia

El proyecto soporta dos modos de persistencia.

## Modo local

Con `USE_SUPABASE=false`, la aplicacion usa `src/storage/database.json`. Este modo sirve para pruebas rapidas sin credenciales.

## Modo Supabase

Con `USE_SUPABASE=true`, la aplicacion usa la tabla configurada en `SUPABASE_TABLE_PRODUCTOS`.

Variables requeridas:

```env
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_TABLE_PRODUCTOS=productos
USE_SUPABASE=true
```

Antes de usar Supabase, ejecuta el archivo `supabase/schema.sql` en el SQL Editor de Supabase.
