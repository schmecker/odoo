import { Component, onMounted, onWillUnmount, useRef, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class WebcamCaptureDialog extends Component {
    static template = "sale_order_webcam_attach.WebcamCaptureDialog";
    static components = { Dialog };
    static props = {
        close: Function,
        resModel: String,
        resId: Number,
    };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.videoRef = useRef("video");
        this.canvasRef = useRef("canvas");
        this.stream = null;
        this.state = useState({
            cameras: [],
            deviceId: "",
            error: "",
            preview: null,
            saving: false,
        });
        onMounted(() => this.startCamera());
        onWillUnmount(() => this.stopStream());
    }

    async refreshDevices() {
        if (!navigator.mediaDevices?.enumerateDevices) {
            return;
        }
        const devices = await navigator.mediaDevices.enumerateDevices();
        this.state.cameras = devices.filter((device) => device.kind === "videoinput");
        if (!this.state.deviceId && this.state.cameras.length) {
            const usbCam = this.state.cameras.find((device) =>
                /usb/i.test(device.label)
            );
            this.state.deviceId = (usbCam || this.state.cameras[0]).deviceId;
        }
    }

    stopStream() {
        if (this.stream) {
            for (const track of this.stream.getTracks()) {
                track.stop();
            }
            this.stream = null;
        }
        if (this.videoRef.el) {
            this.videoRef.el.srcObject = null;
        }
    }

    async startCamera(deviceId = this.state.deviceId) {
        this.state.error = "";
        this.state.preview = null;
        this.stopStream();
        if (!navigator.mediaDevices?.getUserMedia) {
            this.state.error = _t(
                "Ta przeglądarka nie obsługuje kamery. Użyj Chrome lub Edge przez HTTPS."
            );
            return;
        }
        const video = deviceId
            ? { deviceId: { exact: deviceId }, width: { ideal: 1280 }, height: { ideal: 720 } }
            : { width: { ideal: 1280 }, height: { ideal: 720 } };
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: false, video });
        } catch (error) {
            const messages = {
                NotFoundError: _t("Nie znaleziono kamery USB."),
                NotAllowedError: _t("Zezwól przeglądarce na dostęp do kamery."),
                NotReadableError: _t("Kamera jest zajęta przez inną aplikację."),
            };
            this.state.error = messages[error.name] || error.message;
            return;
        }
        if (!this.videoRef.el) {
            this.stopStream();
            return;
        }
        this.videoRef.el.srcObject = this.stream;
        await this.videoRef.el.play();
        await this.refreshDevices();
    }

    async onCameraChange(ev) {
        this.state.deviceId = ev.target.value;
        await this.startCamera(this.state.deviceId);
    }

    capture() {
        const video = this.videoRef.el;
        const canvas = this.canvasRef.el;
        if (!video || !canvas || !video.videoWidth) {
            this.state.error = _t("Poczekaj, aż obraz z kamery będzie gotowy.");
            return;
        }
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);
        this.state.preview = canvas.toDataURL("image/jpeg", 0.92);
        this.state.error = "";
    }

    retake() {
        this.state.preview = null;
    }

    cancel() {
        this.props.close();
    }

    async attach() {
        if (!this.state.preview || this.state.saving) {
            return;
        }
        this.state.saving = true;
        const imageBase64 = this.state.preview.split(",")[1];
        const stamp = new Date().toISOString().replace(/[:.]/g, "-");
        try {
            await this.orm.call(this.props.resModel, "action_attach_webcam_photo", [this.props.resId], {
                image_base64: imageBase64,
                filename: `kamera_${stamp}.jpg`,
            });
            this.notification.add(_t("Zdjęcie zostało załączone przy czacie."), {
                type: "success",
            });
            this.props.close();
            await this.action.doAction({ type: "ir.actions.client", tag: "soft_reload" });
        } catch (error) {
            this.state.error = error.data?.message || error.message || _t("Nie udało się załączyć zdjęcia.");
            this.state.saving = false;
        }
    }
}

export async function openWebcamCapture(env, action) {
    const params = action.params || {};
    const resId = params.res_id || action.context?.active_id;
    if (!resId) {
        env.services.notification.add(_t("Najpierw zapisz zlecenie sprzedaży."), {
            type: "warning",
        });
        return;
    }
    env.services.dialog.add(WebcamCaptureDialog, {
        resModel: params.res_model || "sale.order",
        resId,
    });
}

registry.category("actions").add("sale_order_webcam_capture", openWebcamCapture);
