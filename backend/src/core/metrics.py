"""
Metrics collection and remote write to Amazon Managed Service for Prometheus (AMP)

Note: For production, consider using AWS Distro for OpenTelemetry (ADOT)
or prometheus-remote-write with proper protobuf encoding.
This module provides a placeholder structure.
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class AMPRemoteWrite:
    """
    Placeholder for AMP remote write functionality.

    For production implementation, use one of these approaches:
    1. AWS Distro for OpenTelemetry (ADOT) - recommended
    2. prometheus-remote-write library with protobuf encoding
    3. Sidecar container with prometheus remote write agent
    """

    def __init__(
        self, amp_endpoint: Optional[str] = None, region: Optional[str] = None
    ):
        self.amp_endpoint = amp_endpoint or os.getenv("AMP_REMOTE_WRITE_ENDPOINT")
        self.region = region or os.getenv("AWS_REGION", "eu-west-1")
        self.enabled = bool(self.amp_endpoint)

        if self.enabled:
            logger.info(
                f"AMP endpoint configured: {self.amp_endpoint}. "
                "Note: Remote write not yet implemented. "
                "Metrics are available at /metrics endpoint. "
                "Consider using AWS Distro for OpenTelemetry for production."
            )
        else:
            logger.info(
                "AMP remote write not configured. "
                "Metrics available at /metrics endpoint. "
                "Set AMP_REMOTE_WRITE_ENDPOINT to enable."
            )


# Global instance
_amp_writer: Optional[AMPRemoteWrite] = None


def get_amp_writer() -> Optional[AMPRemoteWrite]:
    """Get or create the AMP remote write instance"""
    global _amp_writer
    if _amp_writer is None:
        _amp_writer = AMPRemoteWrite()
    return _amp_writer
