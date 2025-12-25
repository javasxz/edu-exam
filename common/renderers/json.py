from django.utils import timezone
from rest_framework.renderers import JSONRenderer as BaseJSONRenderer


class JSONRenderer(BaseJSONRenderer):
    """
    Custom json render
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        view = renderer_context.get("view", None)
        response = renderer_context.get("response", None)
        _data = {}

        if not response.exception:
            try:
                message = data.pop("message")
            except:
                message = None
            _data.update(
                status=True,
                message=message,
                data=data or [],
            )
        else:
            _data.update(
                status=False,
                message=data.get("detail", None),
                errors=data.get("errors", []),
            )

        _data.update(
            meta={
                "type": getattr(view, "basename", view.get_view_name()),
                "action": getattr(view, "action", None),
                "titme": timezone.now().isoformat(),
            },
        )

        return super().render(
            _data,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )
