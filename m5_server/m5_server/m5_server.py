#!/usr/bin/env python
# coding:utf-8

from typing import List, Optional

import rclpy
from akari_client import AkariClient
from akari_client.color import Color, Colors
from akari_msgs.srv import (
    SetAllout,
    SetDisplayColor,
    SetDisplayColorRgb,
    SetDisplayImage,
    SetDisplayText,
    SetDout,
    SetPwmout,
    Trigger,
)
from rclpy.node import Node

color_pair: List[str] = [
    "BLACK",
    "NAVY",
    "DARKGREEN",
    "DARKCYAN",
    "MAROON",
    "PURPLE",
    "OLIVE",
    "LIGHTGREY",
    "DARKGREY",
    "BLUE",
    "GREEN",
    "CYAN",
    "RED",
    "MAGENTA",
    "YELLOW",
    "WHITE",
    "ORANGE",
    "GREENYELLOW",
    "PINK",
]


class M5Server(Node):  # type: ignore
    def __init__(self) -> None:
        super().__init__("m5_server_node")
        # create service display color from name
        self._set_display_color_srv = self.create_service(
            SetDisplayColor, "set_display_color", self.set_display_color
        )
        # create service display color from rgb
        self._set_display_color_rgb_srv = self.create_service(
            SetDisplayColorRgb, "set_display_color_rgb", self.set_display_color_rgb
        )
        # create service display text
        self._set_display_text_srv = self.create_service(
            SetDisplayText, "set_display_text", self.set_display_text
        )
        # create service display image
        self._set_display_image_srv = self.create_service(
            SetDisplayImage, "set_display_image", self.set_display_image
        )
        # create service reset m5stack
        self._reset_m5_srv = self.create_service(Trigger, "reset_m5", self.reset_m5)
        # create service dout
        self._set_dout_srv = self.create_service(SetDout, "set_dout", self.set_dout)
        # create service pwmout
        self._set_pwmout_srv = self.create_service(
            SetPwmout, "set_pwmout", self.set_pwmout
        )
        # create service allout
        self._set_allout_srv = self.create_service(
            SetAllout, "set_allout", self.set_allout
        )
        # create service reset allout
        self._reset_allout_srv = self.create_service(
            Trigger, "reset_allout", self.reset_allout
        )
        self.akari = AkariClient()
        self.joints = self.akari.joints
        self.m5 = self.akari.m5stack

    def set_display_color(
        self, request: SetDisplayColor.Request, response: SetDisplayColor.Response
    ) -> SetDisplayColor.Response:
        req_color = request.color.upper()
        sync = request.sync
        response.result = True
        if req_color in color_pair:
            try:
                self.m5.set_display_color(Colors[req_color], sync)
            except BaseException as e:
                self.get_logger().error(e)
                response.result = False
        else:
            self.get_logger().warn(f"Color {req_color} can't display")
            response.result = False
        return response

    def set_display_color_rgb(
        self, request: SetDisplayColorRgb.Request, response: SetDisplayColorRgb.Response
    ) -> SetDisplayColorRgb.Response:
        r_color = request.r
        g_color = request.g
        b_color = request.b
        sync = request.sync
        color = Color(red=r_color, green=g_color, blue=b_color)
        response.result = True
        try:
            self.m5.set_display_color(color, sync=sync)
        except BaseException as e:
            self.get_logger().error(e)
            response.result = False
        return response

    def set_display_text(
        self, request: SetDisplayText.Request, response: SetDisplayText.Response
    ) -> SetDisplayText.Response:
        req_text = request.text
        req_pos_x = request.pos_x
        req_pos_y = request.pos_y
        req_size = request.size
        req_text_color = request.text_color
        req_back_color = request.back_color
        req_refresh = request.refresh
        sync = request.sync
        response.result = True
        if req_text_color not in color_pair:
            self.get_logger().warn(f"Color {req_text_color} can't display")
            response.result = False
            return response
        if req_back_color not in color_pair:
            self.get_logger().warn(f"Color {req_back_color} can't display")
            response.result = False
            return response
        try:
            self.m5.set_display_text(
                text=req_text,
                pos_x=req_pos_x,
                pos_y=req_pos_y,
                size=req_size,
                text_color=Colors[req_text_color],
                back_color=Colors[req_back_color],
                refresh=req_refresh,
                sync=sync,
            )
        except BaseException as e:
            self.get_logger().error(e)
            response.result = False
        return response

    def set_display_image(
        self, request: SetDisplayImage.Request, response: SetDisplayImage.Response
    ) -> SetDisplayImage.Response:
        filepath = request.filepath
        pos_x = request.pos_x
        pos_y = request.pos_y
        scale = request.scale
        sync = request.sync
        response.result = True
        try:
            self.m5.set_display_image(filepath, pos_x, pos_y, scale, sync)
        except BaseException as e:
            self.get_logger().error(e)
            response.result = False
        return response

    def reset_m5(
        self, request: Trigger.Request, response: Trigger.Response
    ) -> Trigger.Response:
        response.result = True
        try:
            self.m5.reset_m5()
        except BaseException as e:
            self.get_logger().error(e)
            response.result = False
        return response

    def set_dout(
        self, request: SetDout.Request, response: SetDout.Response
    ) -> SetDout.Response:
        req_id = request.pin_id
        req_val = request.val
        sync = request.sync
        response.result = True
        if 0 <= req_id <= 1:
            try:
                self.m5.set_dout(req_id, req_val, sync)
            except BaseException as e:
                self.get_logger().error(e)
                response.result = False
        else:
            self.get_logger().warn(
                "PIN_ID is NOT Corect (0-2 is OK): %s" % (str(req_id))
            )
            response.result = False
        return response

    def set_pwmout(
        self, request: SetPwmout.Request, response: SetPwmout.Response
    ) -> SetPwmout.Response:
        req_id = request.pin_id
        req_val = request.val
        sync = request.sync
        response.result = True
        if req_id == 0 and 0 <= req_val < 256:
            try:
                self.m5.set_pwmout(req_id, req_val, sync)
            except BaseException as e:
                self.get_logger().error(e)
                response.result = False
        else:
            self.get_logger().warn(
                "PIN_ID: %s or Value: %s is NOT Corect (ID:0-2, Value:0-255)"
                % (str(req_id), str(req_val))
            )
            response.result = False
        return response

    def set_allout(
        self, request: SetAllout.Request, response: SetAllout.Response
    ) -> SetAllout.Response:
        req_dout0 = request.dout0_val
        req_dout1 = request.dout1_val
        req_pwmout0_val = request.pwmout0_val
        sync = request.sync
        response.result = True
        if 0 <= req_pwmout0_val < 256:
            try:
                self.m5.set_allout(
                    dout0=req_dout0, dout1=req_dout1, pwmout0=req_pwmout0_val, sync=sync
                )
            except BaseException as e:
                self.get_logger().error(e)
                response.result = False
        else:
            self.get_logger().warn(
                "PWM Value: %s is NOT Corect (0-255)" % (str(req_pwmout0_val))
            )
            response.result = False
        return response

    def reset_allout(
        self, request: Trigger.Request, response: Trigger.Response
    ) -> Trigger.Response:
        response.result = True
        try:
            self.m5.reset_allout()
        except BaseException as e:
            self.get_logger().error(e)
            response.result = False
        return response


def main(args: Optional[str] = None) -> None:
    rclpy.init(args=args)
    server = M5Server()
    rclpy.spin(server)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
