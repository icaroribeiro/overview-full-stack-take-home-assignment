import json
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask_restx import Namespace, Resource, fields, reqparse
from src import AppContainer
from src.controller.dto.videos import UploadImageResponse, VideoResponse
from src.infrastructure import application_settings
from src.service.file import FileService
from src.service.video import VideoService
from src.utils.api_exceptions import NoContentException
from src.utils.json_response import respond_with_json
from werkzeug.datastructures import FileStorage

api = Namespace(name="videos", description="Videos related operations")

create_video_parser = reqparse.RequestParser()
create_video_parser.add_argument("name", location="json", type=str, required=True)

get_videos_parser = reqparse.RequestParser()
get_videos_parser.add_argument(
    "name",
    location="args",
    type=str,
    required=False,
)

upload_image_parser = reqparse.RequestParser()
upload_image_parser.add_argument(
    "file", location="files", type=FileStorage, required=True
)

video_response_fields = api.model(
    name="VideoResponse",
    model={
        "id": fields.String(),
        "name": fields.String(),
        "image_path_list": fields.List(fields.String()),
        "created_at": fields.Date(),
    },
)
video_error_response_fields = api.model(
    "VideoErrorResponse",
    {"message": fields.String(), "extra": fields.String()},
)
videos_response_fields = [video_response_fields]
videos_error_response_fields = api.model(
    "GetVideosErrorResponse",
    {"message": fields.String(), "extra": fields.String()},
)

upload_image_response_fields = api.model(
    "UploadImageResponse", {"path": fields.String()}
)
upload_image_error_response_fields = api.model(
    "UploadImageErrorResponse", {"message": fields.String(), "extra": fields.String()}
)


@api.route("/<string:video_id>/upload-image")
class UploadImage(Resource):
    @inject
    def __init__(
        self,
        api=None,
        file_service: FileService = Provide[AppContainer.service.file_service],
        video_service: VideoService = Provide[AppContainer.service.video_service],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.file_service = file_service
        self.video_service = video_service

    @api.response(code=200, model=upload_image_response_fields, description="OK")
    def post(self, video_id: str):
        args = upload_image_parser.parse_args()

        if "file" not in args:
            raise NoContentException(
                extra="The request performed without the file part"
            )

        file = args["file"]

        allowed_extensions = application_settings.allowed_image_extensions

        image_path = self.file_service.save_file(
            file=file, allowed_extensions=allowed_extensions
        )

        self.video_service.renew_image_path_list(id=video_id, image_path=image_path)

        return respond_with_json(
            payload=UploadImageResponse(path=image_path).json(),
            code=HTTPStatus.OK.value,
        )


@api.route("")
class Videos(Resource):
    @inject
    def __init__(
        self,
        api=None,
        video_service: VideoService = Provide[AppContainer.service.video_service],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.video_service = video_service

    @api.doc("create_video")
    @api.expect(create_video_parser)
    @api.response(
        code=HTTPStatus.CREATED.value,
        model=video_response_fields,
        description="Created",
    )
    @api.response(
        code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        model=video_error_response_fields,
        description="Internal Server Error",
    )
    def post(self):
        args = create_video_parser.parse_args()
        name = args.get("name")

        video = self.video_service.save_video(name)

        return respond_with_json(
            payload=VideoResponse.from_domain(video=video).json(),
            code=HTTPStatus.CREATED.value,
        )

    @api.doc("get_videos")
    @api.expect(get_videos_parser)
    @api.response(
        code=HTTPStatus.OK.value,
        model=videos_response_fields,
        description="OK",
    )
    @api.response(
        code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        model=videos_error_response_fields,
        description="Internal Server Error",
    )
    def get(self):
        args = get_videos_parser.parse_args()
        name = args.get("name")

        video_list = self.video_service.retrieve_videos(name=name)

        list_videos_response = [
            json.loads(VideoResponse.from_domain(video=video).json())
            for video in video_list
        ]

        return respond_with_json(payload=list_videos_response, code=HTTPStatus.OK.value)
