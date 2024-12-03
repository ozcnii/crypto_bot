interface HotAlertProps {
  index: number;
}

export const HotAlert = ({ index }: HotAlertProps) => {
  return (
    <div>
      <span className="alert alert-danger">Hot</span>
      <span>{index}</span>
    </div>
  );
};
