
INSERT INTO public.items (
    dashboard_id,
    dashboard_name,
    dashboard_url,
    dashboard_description,
    dashboard_icon,
    option_type,
    created_by
)
VALUES ( %s, %s, %s, %s, %s, %s, %s);