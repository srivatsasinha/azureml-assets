# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Scoring request."""

import json
import uuid

from ...utils.json_encoder_extensions import BatchComponentJSONEncoder
from ..post_processing.mini_batch_context import MiniBatchContext
from ..request_modification.input_transformer import InputTransformer
from .scoring_attempt import ScoringAttempt


class ScoringRequest:
    """Scoring request."""

    __BATCH_REQUEST_METADATA = "_batch_request_metadata"
    __REQUEST_METADATA = "request_metadata"
<<<<<<< HEAD
=======
    __CUSTOM_ID = "custom_id"
>>>>>>> 7a54b91f3a492ed00e3033a99450bbc4df36a0fa

    def __init__(
            self,
            original_payload: str,
            input_to_request_transformer: InputTransformer = None,
            input_to_log_transformer: InputTransformer = None,
            internal_id: str = None,
            mini_batch_context: MiniBatchContext = None):
        """Initialize ScoringRequest."""
        self.__original_payload = original_payload
        self.__original_payload_obj = json.loads(original_payload)
        self.__input_to_request_transformer = input_to_request_transformer
        self.__input_to_log_transformer = input_to_log_transformer
        self.__internal_id: str = internal_id or str(uuid.uuid4())

        # Used in checking if the max_retry_time_interval has been exceeded
        self.scoring_duration: int = 0

        # Duplicate original payload obj, to not change the original
        self.__cleaned_payload_obj = json.loads(original_payload)
        self.__loggable_payload_obj = json.loads(original_payload)

        # Apply any modifiers to the original payload
        if self.__input_to_request_transformer:
            self.__cleaned_payload_obj = self.__input_to_request_transformer.apply_modifications(
                self.__cleaned_payload_obj)

        if self.__input_to_log_transformer:
            self.__loggable_payload_obj = self.__input_to_log_transformer.apply_modifications(
                self.__loggable_payload_obj)

        # Pop _batch_request_metadata property from payload, if present
        # Override with request_metadata, if present
        # In case both exist, we call pop twice to make sure these properties
        # are removed from the cleaned payload object
        # These properties do not need to be sent to the model & will be added to the output file directly
        self.__request_metadata = self.__cleaned_payload_obj.pop(self.__BATCH_REQUEST_METADATA, None)
        self.__request_metadata = self.__cleaned_payload_obj.pop(self.__REQUEST_METADATA, self.__request_metadata)
<<<<<<< HEAD
=======
        # If custom_id exists (V2 input schema), make sure it is not sent to MIR endpoint
        self.__CUSTOM_ID = self.__cleaned_payload_obj.pop(self.__CUSTOM_ID, None)
>>>>>>> 7a54b91f3a492ed00e3033a99450bbc4df36a0fa

        self.__cleaned_payload = json.dumps(self.__cleaned_payload_obj, cls=BatchComponentJSONEncoder)
        self.__loggable_payload = json.dumps(self.__loggable_payload_obj, cls=BatchComponentJSONEncoder)

        self.__estimated_cost: int = None
        self.__estimated_tokens_per_item_in_batch: tuple[int] = ()
        self.__segment_id: int = None
        self.__scoring_url: str = None

        self.mini_batch_context: MiniBatchContext = mini_batch_context
        self.request_history: list[ScoringAttempt] = []  # Stack
        self.retry_count: int = 0
        self.retry_count_for_limited_retries: int = 0
        self.total_wait_time: int = 0

    # read-only
    @property
    def internal_id(self):
        """Internal id."""
        return self.__internal_id

    # read-only
    @property
    def original_payload(self):
        """Original payload."""
        return self.__original_payload

    # read-only
    @property
    def original_payload_obj(self):
        """Original payload object."""
        return self.__original_payload_obj

    # read-only
    @property
    def cleaned_payload(self):
        """Cleaned original payload."""
        return self.__cleaned_payload

    # read-only
    @property
    def cleaned_payload_obj(self):
        """Cleaned original payload object."""
        return self.__cleaned_payload_obj

    # read-only
    @property
    def loggable_payload(self):
        """Loggable payload."""
        return self.__loggable_payload

    # read-only
    @property
    def request_metadata(self):
        """Request metadata."""
        return self.__request_metadata

    # read-only
    @property
    def estimated_cost(self) -> int:
        """Get the estimated cost."""
        return self.__estimated_cost or sum(self.__estimated_tokens_per_item_in_batch)

    # read-only
    @property
    def estimated_token_counts(self) -> "tuple[int]":
        """Get the estimated token counts."""
        return self.__estimated_tokens_per_item_in_batch

    # read-only
    @property
    def scoring_url(self) -> str:
        """Get the scoring url."""
        return self.__scoring_url

    # read-only
    @property
    def segment_id(self) -> int:
        """Get the segment id."""
        return self.__segment_id

<<<<<<< HEAD
=======
    # read-only
    @property
    def custom_id(self) -> str:
        """Get the custom id. Only valid for V2 input schema."""
        return self.__CUSTOM_ID

>>>>>>> 7a54b91f3a492ed00e3033a99450bbc4df36a0fa
    @estimated_cost.setter
    def estimated_cost(self, cost: int):
        """Set the estimated cost."""
        self.__estimated_cost = cost

    @scoring_url.setter
    def scoring_url(self, url: str):
        """Set the scoring url."""
        self.__scoring_url = url

    @segment_id.setter
    def segment_id(self, id: int):
        """Set the segment id."""
        self.__segment_id = id

    @estimated_token_counts.setter
    def estimated_token_counts(self, token_counts: "tuple[int]"):
        """Set the estimated token counts."""
        self.__estimated_tokens_per_item_in_batch = token_counts

    def copy_with_new_payload(self, payload):
        """Create a copy of the ScoringRequest using the existing transformers on a new payload."""
        return ScoringRequest(
            original_payload=payload,
            internal_id=self.__internal_id,
            input_to_request_transformer=self.__input_to_request_transformer,
            input_to_log_transformer=self.__input_to_log_transformer,
            mini_batch_context=self.mini_batch_context,
        )
