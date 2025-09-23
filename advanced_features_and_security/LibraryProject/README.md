DJANGO PROJECT

# Groups & Permissions Setup

## Custom Permissions
The `Book` model defines the following permissions:
- can_view
- can_create
- can_edit
- can_delete

## Groups
Create these groups via Django Admin:
- **Viewers** → [can_view]
- **Editors** → [can_view, can_create, can_edit]
- **Admins** → [can_view, can_create, can_edit, can_delete]

## Usage in Views
- Views are protected with @permission_required.
- Example: @permission_required('yourapp.can_edit', raise_exception=True)
- Unauthorized users will see a 403 error.

## Testing
1. Create users in Django Admin.
2. Assign them to one of the groups.
3. Log in as each user and test access to book-related views.
