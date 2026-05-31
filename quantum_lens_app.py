import cv2
from prime_mathematician import PrimeMathematicianAI
from virtual_camera import VirtualCamera

class QuantumLensApp:
    def __init__(self, camera_source=0):
        self.cam = VirtualCamera(camera_source)
        self.ai = PrimeMathematicianAI()

    def run(self):
        while True:
            frame = self.cam.get_frame()
            if frame is None:
                break

            profiles = self.ai.analyze_image(frame)

            # Here is where we "see mathematics":
            # overlay primes, log them, or stream them elsewhere
            for profile in profiles:
                primes = [sp.value for sp in profile.quantum_state.candidates]
                print(f"Person {profile.person_id}: {primes}")

            key = cv2.waitKey(1) & 0xFF

            # 's' = virtual selfie (collapse your own prime)
            if key == ord('s'):
                if profiles:
                    chosen = self.ai.observe_person(profiles[0])
                    print(f"✨ Quantum selfie: {chosen.value} ({chosen.charge}, {chosen.spin}, {chosen.phase})")

            # 'q' = quit
            if key == ord('q'):
                break

        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QuantumLensApp()
    app.run()
